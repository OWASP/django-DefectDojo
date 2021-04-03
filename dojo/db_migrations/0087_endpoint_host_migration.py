# Generated by Django 2.2.18 on 2021-03-24 21:48
import logging
import re

from django.core.validators import validate_ipv46_address
from django.db import migrations
from django.core.exceptions import FieldError, ValidationError

from dojo.models import Endpoint

logger = logging.getLogger(__name__)


def clean_hosts(apps, schema_editor):
    broken_endpoints = []
    Endpoint_model = apps.get_model('dojo', 'Endpoint')
    error_prefix = 'It is not possible to migrate it. Remove or fix this endpoint.'
    for endpoint in Endpoint_model.objects.all():
        if not endpoint.host or endpoint.host == '':
            logger.error('Endpoint (id={}) does have "host" field, {}'.format(endpoint.pk, error_prefix))
            broken_endpoints.append(endpoint.pk)
        else:
            if not re.match(r'^[A-Za-z][A-Za-z0-9\.\-\+]+$', endpoint.host):  # is old host valid FQDN?
                try:
                    validate_ipv46_address(endpoint.host)  # is old host valid IPv4/6?
                except ValidationError:
                    try:
                        if '://' in endpoint.host:  # is the old host full uri?
                            parts = Endpoint.from_uri(endpoint.host)
                            # can raise exception if the old host is not valid URL
                        else:
                            parts = Endpoint.from_uri('//' + endpoint.host)
                            # can raise exception if there is no way to parse the old host

                        if parts.protocol:
                            if endpoint.protocol and (endpoint.protocol != parts.protocol):
                                logger.error('Endpoint (id={}) has defined protocol ({}) and it not same as protocol'
                                             ' in host ({}). {}'.format(endpoint.pk, endpoint.protocol, parts.protocol,
                                                                        error_prefix))
                                broken_endpoints.append(endpoint.pk)
                            else:
                                endpoint.protocol = parts.protocol

                        if parts.userinfo:
                            endpoint.userinfo = parts.userinfo

                        if parts.host:
                            endpoint.host = parts.host
                        else:
                            logger.error('Endpoint (id={}) "{}" use invalid format of host. {}'.format(endpoint.pk, endpoint.host, error_prefix))
                            broken_endpoints.append(endpoint.pk)

                        if parts.port:
                            try:
                                if (endpoint.port is not None) and (int(endpoint.port) != parts.port):
                                    logger.error('Endpoint (id={}) has defined port number ({}) and it not same as '
                                                 'port number in host ({}). {}'.format(endpoint.pk, endpoint.port,
                                                                                     parts.port, error_prefix))
                                    broken_endpoints.append(endpoint.pk)
                                else:
                                    endpoint.port = parts.port
                            except ValueError:
                                logger.error('Endpoint (id={}) use non-numeric port: {}. {}'.format(endpoint.pk,
                                                                                                    endpoint.port,
                                                                                                    error_prefix))
                                broken_endpoints.append(endpoint.pk)

                        if parts.path:
                            if endpoint.path and (endpoint.path != parts.path):
                                logger.error('Endpoint (id={}) has defined path ({}) and it not same as path in host '
                                             '({}). {}'.format(endpoint.pk, endpoint.path, parts.path, error_prefix))
                                broken_endpoints.append(endpoint.pk)
                            else:
                                endpoint.path = parts.path

                        if parts.query:
                            if endpoint.query and (endpoint.query != parts.query):
                                logger.error('Endpoint (id={}) has defined query ({}) and it not same as query in host '
                                             '({}). {}'.format(endpoint.pk, endpoint.query, parts.query, error_prefix))
                                broken_endpoints.append(endpoint.pk)
                            else:
                                endpoint.query = parts.query

                        if parts.fragment:
                            if endpoint.fragment and (endpoint.fragment != parts.fragment):
                                logger.error('Endpoint (id={}) has defined fragment ({}) and it not same as fragment '
                                             'in host ({}). {}'.format(endpoint.pk, endpoint.fragment, parts.fragment,
                                                                       error_prefix))
                                broken_endpoints.append(endpoint.pk)
                            else:
                                endpoint.fragment = parts.fragment

                        endpoint.save()

                    except ValidationError:
                        logger.error('Endpoint (id={}) "{}" use invalid format of host. {}'.format(endpoint.pk, endpoint.host, error_prefix))
                        broken_endpoints.append(endpoint.pk)
    if broken_endpoints != []:
        raise FieldError('It is not possible to migrate database because there is/are {} broken endpoint(s). '
                         'Please check logs.'.format(len(broken_endpoints)))


class Migration(migrations.Migration):
    dependencies = [
        ('dojo', '0086_endpoint_userinfo_creation'),
    ]

    operations = [
        # This step wasn't possible to merge with 0086_endpoint_userinfo_creation, because Unittest shows:
        # django.db.utils.OperationalError: (1060, "Duplicate column name 'userinfo'")
        migrations.RunPython(clean_hosts)
    ]