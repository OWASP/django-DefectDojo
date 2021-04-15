from django.db.models.signals import post_delete, pre_delete
from django.dispatch.dispatcher import receiver
from dojo.celery import app
from dojo.decorators import dojo_async_task, dojo_model_from_id, dojo_model_to_id
import logging
from time import strftime
from django.utils import timezone
from django.conf import settings
from fieldsignals import pre_save_changed
from dojo.utils import get_current_user, mass_model_updater, to_str_typed
from dojo.models import Engagement, Finding, Finding_Group, System_Settings, Test


logger = logging.getLogger(__name__)
deduplicationLogger = logging.getLogger("dojo.specific-loggers.deduplication")


# this signal is triggered just before a finding is getting saved
# and one of the status related fields has changed
# this allows us to:
# - set any depending fields such as mitigated_by, mitigated, etc.
# - update any audit log / status history
def pre_save_finding_status_change(sender, instance, changed_fields=None, **kwargs):
    # some code is cloning findings by setting id/pk to None, ignore those, will be handled on next save
    # if not instance.id:
    #     logger.debug('ignoring save of finding without id')
    #     return

    logger.debug('%i: changed status fields pre_save: %s', instance.id or 0, changed_fields)

    for field, (old, new) in changed_fields.items():
        logger.debug("%i: %s changed from %s to %s" % (instance.id or 0, field, old, new))
        user = None
        if get_current_user() and get_current_user().is_authenticated:
            user = get_current_user()
        update_finding_status(instance, user, changed_fields)


# also get signal when id is set/changed so we can process new findings
pre_save_changed.connect(pre_save_finding_status_change, sender=Finding, fields=['id', 'active', 'verfied', 'false_p', 'is_Mitigated', 'mitigated', 'mitigated_by', 'out_of_scope', 'risk_accepted'])
# pre_save_changed.connect(pre_save_finding_status_change, sender=Finding)
# post_save_changed.connect(pre_save_finding_status_change, sender=Finding, fields=['active', 'verfied', 'false_p', 'is_Mitigated', 'mitigated', 'mitigated_by', 'out_of_scope'])


def update_finding_status(new_state_finding, user, changed_fields=None):
    now = timezone.now()

    is_new_finding = changed_fields and len(changed_fields) == 1 and 'id' in changed_fields

    # activated
    # reactivated
    # closed / mitigated
    # false positivized
    # out_of_scopified
    # marked as duplicate
    # marked as original

    if 'is_Mitigated' in changed_fields or is_new_finding:
        # finding is being mitigated
        if new_state_finding.is_Mitigated:
            # when mitigating a finding, the meta fields can only be editted if allowed
            logger.debug('finding being mitigated, set mitigated and mitigated_by fields')

            if can_edit_mitigated_data(user):
                # only set if it was not already set by user
                # not sure if this check really covers all cases, but if we make it more strict
                # it will cause all kinds of issues I believe with new findings etc
                new_state_finding.mitigated = new_state_finding.mitigated or now
                new_state_finding.mitigated_by = new_state_finding.mitigated_by or user

        # finding is being "un"mitigated
        else:
            new_state_finding.mitigated = None
            new_state_finding.mitigated_by = None

    # people may try to remove mitigated/mitigated_by by accident
    if new_state_finding.is_Mitigated:
        new_state_finding.mitigated = new_state_finding.mitigated or now
        new_state_finding.mitigated_by = new_state_finding.mitigated_by or user

    if 'active' in changed_fields or is_new_finding:
        # finding is being (re)activated
        if new_state_finding.active:
            new_state_finding.false_p = False
            new_state_finding.out_of_scope = False
            new_state_finding.is_Mitigated = False
            new_state_finding.mitigated = None
            new_state_finding.mitigated_by = None
        else:
            # finding is being deactivated
            pass

    if 'verified' in changed_fields or is_new_finding:
        pass

    if 'false_p' in changed_fields or 'out_of_scope' in changed_fields or is_new_finding:
        # existing behaviour is that false_p or out_of_scope implies mitigated
        if new_state_finding.false_p or new_state_finding.out_of_scope:
            new_state_finding.mitigated = new_state_finding.mitigated or now
            new_state_finding.mitigated_by = new_state_finding.mitigated_by or user
            new_state_finding.is_Mitigated = True
            new_state_finding.active = False
            new_state_finding.verified = False

    # always reset some fields if the finding is not a duplicate
    if not new_state_finding.duplicate:
        new_state_finding.duplicate = False
        new_state_finding.duplicate_finding = None

    new_state_finding.last_status_update = now


def can_edit_mitigated_data(user):
    return settings.EDITABLE_MITIGATED_DATA and user.is_superuser


def create_finding_group(finds, finding_group_name):
    logger.debug('creating finding_group_create')
    if not finds or len(finds) == 0:
        raise ValueError('cannot create empty Finding Group')

    finding_group_name_dummy = 'bulk group ' + strftime("%a, %d %b  %Y %X", timezone.now().timetuple())

    finding_group = Finding_Group(test=finds[0].test)
    finding_group.creator = get_current_user()
    finding_group.name = finding_group_name + finding_group_name_dummy
    finding_group.save()
    available_findings = [find for find in finds if not find.finding_group_set.all()]
    finding_group.findings.set(available_findings)

    # if user provided a name, we use that, else:
    # if we have components, we may set a nice name but catch 'name already exist' exceptions
    try:
        if finding_group_name:
            finding_group.name = finding_group_name
        elif finding_group.components:
            finding_group.name = finding_group.components
        finding_group.save()
    except:
        pass

    added = len(available_findings)
    skipped = len(finds) - added
    return finding_group, added, skipped


def add_to_finding_group(finding_group, finds):
    added = 0
    skipped = 0
    available_findings = [find for find in finds if not find.finding_group_set.all()]
    finding_group.findings.add(*available_findings)

    added = len(available_findings)
    skipped = len(finds) - added
    return finding_group, added, skipped


def remove_from_finding_group(finds):
    removed = 0
    skipped = 0
    affected_groups = []
    for find in finds:
        groups = find.finding_group_set.all()
        if not groups:
            skipped += 1
            continue

        for group in find.finding_group_set.all():
            group.findings.remove(find)
            affected_groups.append(group)

        removed += 1

    return affected_groups, removed, skipped


@dojo_model_to_id
@dojo_async_task
@app.task
@dojo_model_from_id
def post_process_finding_save(finding, dedupe_option=True, false_history=False, rules_option=True, product_grading_option=True,
             issue_updater_option=True, push_to_jira=False, user=None, *args, **kwargs):

    system_settings = System_Settings.objects.get()

    # STEP 1 run all status changing tasks sequentially to avoid race conditions
    if dedupe_option:
        if finding.hash_code is not None:
            if system_settings.enable_deduplication:
                from dojo.utils import do_dedupe_finding
                do_dedupe_finding(finding, *args, **kwargs)
            else:
                deduplicationLogger.debug("skipping dedupe because it's disabled in system settings")
        else:
            deduplicationLogger.warning("skipping dedupe because hash_code is None")

    if false_history:
        if system_settings.false_positive_history:
            from dojo.utils import do_false_positive_history
            do_false_positive_history(finding, *args, **kwargs)
        else:
            deduplicationLogger.debug("skipping false positive history because it's disabled in system settings")

    # STEP 2 run all non-status changing tasks as celery tasks in the background
    if issue_updater_option:
        from dojo.tools import tool_issue_updater
        tool_issue_updater.async_tool_issue_update(finding)

    if product_grading_option:
        if system_settings.enable_product_grade:
            from dojo.utils import calculate_grade
            calculate_grade(finding.test.engagement.product)
        else:
            deduplicationLogger.debug("skipping product grading because it's disabled in system settings")

    # Adding a snippet here for push to JIRA so that it's in one place
    if push_to_jira:
        logger.debug('pushing finding %s to jira from finding.save()', finding.pk)
        import dojo.jira_link.helper as jira_helper
        jira_helper.push_to_jira(finding)


@receiver(pre_delete, sender=Finding)
def finding_pre_delete(sender, instance, **kwargs):
    # this shouldn't be necessary as Django should remove any Many-To-Many entries automatically, might be a bug in Django?
    # https://code.djangoproject.com/ticket/154
    logger.debug('finding pre_delete: %d', instance.id)

    # instance.found_by.clear()
    # instance.status_finding.clear()


def finding_delete(instance, **kwargs):
    logger.debug('finding delete, instance: %s', instance.id)

    # the idea is that the engagement/test pre delete already prepared all the duplicates inside
    # the test/engagement to no longer point to any original so they can be safely deleted.
    # so if we still find that the finding that is going to be delete is an original, it is either
    # a manual / single finding delete, or a bulke delete of findings
    # in which case we have to process all the duplicates
    # TODO: should we add the prepocessing also to the bulk edit form?
    logger.debug('finding_delete: refresh from db: pk: %d', instance.pk)

    try:
        instance.refresh_from_db()
    except Finding.DoesNotExist:
        # due to cascading deletes, the current finding could have been deleted already
        # but django still calls delete() in this case
        return

    duplicate_cluster = instance.original_finding.all()
    if duplicate_cluster:
        reconfigure_duplicate_cluster(instance, duplicate_cluster)
    else:
        logger.debug('no duplicate cluster found for finding: %d, so no need to reconfigure', instance.id)

    # this shouldn't be necessary as Django should remove any Many-To-Many entries automatically, might be a bug in Django?
    # https://code.djangoproject.com/ticket/154
    logger.debug('finding delete: clearing found by')
    instance.found_by.clear()
    instance.status_finding.clear()


@receiver(post_delete, sender=Finding)
def finding_post_delete(sender, instance, **kwargs):
    logger.debug('finding post_delete, sender: %s instance: %s', to_str_typed(sender), to_str_typed(instance))
    # calculate_grade(instance.test.engagement.product)


def reset_duplicate_before_delete(dupe):
    dupe.duplicate_finding = None
    dupe.duplicate = False


def reset_duplicates_before_delete(qs):
    mass_model_updater(Finding, qs, lambda f: reset_duplicate_before_delete(f), fields=['duplicate', 'duplicate_finding'])


def set_new_original(finding, new_original):
    if finding.duplicate:
        finding.duplicate_finding = new_original


# can't use model to id here due to the queryset
# @dojo_async_task
# @app.task
def reconfigure_duplicate_cluster(original, cluster_outside):
    # when a finding is deleted, and is an original of a duplicate cluster, we have to chose a new original for the cluster
    # only look for a new original if there is one outside this test
    if original is None or cluster_outside is None or len(cluster_outside) == 0:
        return

    if settings.DUPLICATE_CLUSTER_CASCADE_DELETE:
        cluster_outside.order_by('-id').delete()
    else:
        logger.debug('reconfigure_duplicate_cluster: cluster_outside: %s', cluster_outside)
        # set new original to first finding in cluster (ordered by id)
        new_original = cluster_outside.order_by('id').first()
        if new_original:
            logger.debug('changing original of duplicate cluster %d to: %s:%s', original.id, new_original.id, new_original.title)

            new_original.duplicate = False
            new_original.duplicate_finding = None
            new_original.active = True
            new_original.save_no_options()
            new_original.found_by.set(original.found_by.all())

        # if the cluster is size 1, there's only the new original left
        if new_original and len(cluster_outside) > 1:
            # for find in cluster_outside:
            #     if find != new_original:
            #         find.duplicate_finding = new_original
            #         find.save_no_options()

            mass_model_updater(Finding, cluster_outside, lambda f: set_new_original(f, new_original), fields=['duplicate_finding'])


def prepare_duplicates_for_delete(test=None, engagement=None):
    logger.debug('prepare duplicates for delete, test: %s, engagement: %s', test.id if test else None, engagement.id if engagement else None)
    if test is None and engagement is None:
        logger.warn('nothing to prepare as test and engagement are None')

    # get all originals in the test/engagement
    originals = Finding.objects.filter(original_finding__isnull=False)
    if engagement:
        originals = originals.filter(test__engagement=engagement)
    if test:
        originals = originals.filter(test=test)

    # use distinct to flatten the join result
    originals = originals.distinct()

    if len(originals) == 0:
        logger.debug('no originals found, so no duplicates to prepare for deletion of original')
        return

    # remove the link to the original from the duplicates inside the cluster so they can be safely deleted by the django framework
    total = len(originals)
    i = 0
    # logger.debug('originals: %s', [original.id for original in originals])
    for original in originals:
        i += 1
        logger.debug('%d/%d: preparing duplicate cluster for deletion of original: %d', i, total, original.id)
        cluster_inside = original.original_finding.all()
        if engagement:
            cluster_inside = cluster_inside.filter(test__engagement=engagement)

        if test:
            cluster_inside = cluster_inside.filter(test=test)

        if len(cluster_inside) > 0:
            reset_duplicates_before_delete(cluster_inside)

        # reconfigure duplicates outside test/engagement
        cluster_outside = original.original_finding.all()
        if engagement:
            cluster_outside = cluster_outside.exclude(test__engagement=engagement)

        if test:
            cluster_outside = cluster_outside.exclude(test=test)

        if len(cluster_outside) > 0:
            reconfigure_duplicate_cluster(original, cluster_outside)

        logger.debug('done preparing duplicate cluster for deletion of original: %d', original.id)


@receiver(pre_delete, sender=Test)
def test_pre_delete(sender, instance, **kwargs):
    logger.debug('test pre_delete, sender: %s instance: %s', to_str_typed(sender), to_str_typed(instance))
    prepare_duplicates_for_delete(test=instance)


@receiver(post_delete, sender=Test)
def test_post_delete(sender, instance, **kwargs):
    logger.debug('test post_delete, sender: %s instance: %s', to_str_typed(sender), to_str_typed(instance))


@receiver(pre_delete, sender=Engagement)
def engagement_pre_delete(sender, instance, **kwargs):
    logger.debug('engagement pre_delete, sender: %s instance: %s', to_str_typed(sender), to_str_typed(instance))
    prepare_duplicates_for_delete(engagement=instance)


@receiver(post_delete, sender=Engagement)
def engagement_post_delete(sender, instance, **kwargs):
    logger.debug('engagement post_delete, sender: %s instance: %s', to_str_typed(sender), to_str_typed(instance))
