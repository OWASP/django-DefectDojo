# Generated by Django 2.2.1 on 2019-09-22 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dojo", "0022_google_sheet_sync_additions"),
    ]

    operations = [
        migrations.AddField(
            model_name="finding",
            name="nb_occurences",
            field=models.IntegerField(
                blank=True,
                help_text="Number of occurences in the source tool when several vulnerabilites were found and aggregated by the scanner",
                null=True,
                verbose_name="Number of occurences",
            ),
        ),
        migrations.AddField(
            model_name="finding",
            name="sast_sink_object",
            field=models.CharField(
                blank=True,
                help_text="Sink object (variable, function...) of the attack vector",
                max_length=500,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="finding",
            name="sast_source_file_path",
            field=models.CharField(
                blank=True,
                help_text="Source filepath of the attack vector",
                max_length=4000,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="finding",
            name="sast_source_line",
            field=models.IntegerField(
                blank=True,
                help_text="Source line number of the attack vector",
                null=True,
                verbose_name="Line number",
            ),
        ),
        migrations.AddField(
            model_name="finding",
            name="sast_source_object",
            field=models.CharField(
                blank=True,
                help_text="Source object (variable, function...) of the attack vector",
                max_length=500,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="finding",
            name="unique_id_from_tool",
            field=models.CharField(
                blank=True,
                help_text="Vulnerability technical id from the source tool. Allows to track unique vulnerabilities",
                max_length=500,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="child_rule",
            name="match_field",
            field=models.CharField(
                choices=[
                    ("id", "id"),
                    ("title", "title"),
                    ("date", "date"),
                    ("cwe", "cwe"),
                    ("cve", "cve"),
                    ("url", "url"),
                    ("severity", "severity"),
                    ("description", "description"),
                    ("mitigation", "mitigation"),
                    ("impact", "impact"),
                    ("steps_to_reproduce", "steps_to_reproduce"),
                    ("severity_justification", "severity_justification"),
                    ("references", "references"),
                    ("test", "test"),
                    ("is_template", "is_template"),
                    ("active", "active"),
                    ("verified", "verified"),
                    ("false_p", "false_p"),
                    ("duplicate", "duplicate"),
                    ("duplicate_finding", "duplicate_finding"),
                    ("out_of_scope", "out_of_scope"),
                    ("under_review", "under_review"),
                    ("review_requested_by", "review_requested_by"),
                    ("under_defect_review", "under_defect_review"),
                    ("defect_review_requested_by", "defect_review_requested_by"),
                    ("is_Mitigated", "is_Mitigated"),
                    ("thread_id", "thread_id"),
                    ("mitigated", "mitigated"),
                    ("mitigated_by", "mitigated_by"),
                    ("reporter", "reporter"),
                    ("numerical_severity", "numerical_severity"),
                    ("last_reviewed", "last_reviewed"),
                    ("last_reviewed_by", "last_reviewed_by"),
                    ("line_number", "line_number"),
                    ("sourcefilepath", "sourcefilepath"),
                    ("sourcefile", "sourcefile"),
                    ("param", "param"),
                    ("payload", "payload"),
                    ("hash_code", "hash_code"),
                    ("line", "line"),
                    ("file_path", "file_path"),
                    ("static_finding", "static_finding"),
                    ("dynamic_finding", "dynamic_finding"),
                    ("created", "created"),
                    ("jira_creation", "jira_creation"),
                    ("jira_change", "jira_change"),
                    ("scanner_confidence", "scanner_confidence"),
                    ("sonarqube_issue", "sonarqube_issue"),
                    ("unique_id_from_tool", "unique_id_from_tool"),
                    ("sast_source_object", "sast_source_object"),
                    ("sast_sink_object", "sast_sink_object"),
                    ("sast_source_line", "sast_source_line"),
                    ("sast_source_file_path", "sast_source_file_path"),
                    ("nb_occurences", "nb_occurences"),
                ],
                max_length=200,
            ),
        ),
        migrations.AlterField(
            model_name="finding",
            name="file_path",
            field=models.CharField(
                blank=True,
                help_text="File name with path. For SAST, when source (start of the attack vector) and sink (end of the attack vector) information are available, put sink information here",
                max_length=4000,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="finding",
            name="line",
            field=models.IntegerField(
                blank=True,
                help_text="Line number. For SAST, when source (start of the attack vector) and sink (end of the attack vector) information are available, put sink information here",
                null=True,
                verbose_name="Line number",
            ),
        ),
        migrations.AlterField(
            model_name="rule",
            name="applied_field",
            field=models.CharField(
                choices=[
                    ("id", "id"),
                    ("title", "title"),
                    ("date", "date"),
                    ("cwe", "cwe"),
                    ("cve", "cve"),
                    ("url", "url"),
                    ("severity", "severity"),
                    ("description", "description"),
                    ("mitigation", "mitigation"),
                    ("impact", "impact"),
                    ("steps_to_reproduce", "steps_to_reproduce"),
                    ("severity_justification", "severity_justification"),
                    ("references", "references"),
                    ("test", "test"),
                    ("is_template", "is_template"),
                    ("active", "active"),
                    ("verified", "verified"),
                    ("false_p", "false_p"),
                    ("duplicate", "duplicate"),
                    ("duplicate_finding", "duplicate_finding"),
                    ("out_of_scope", "out_of_scope"),
                    ("under_review", "under_review"),
                    ("review_requested_by", "review_requested_by"),
                    ("under_defect_review", "under_defect_review"),
                    ("defect_review_requested_by", "defect_review_requested_by"),
                    ("is_Mitigated", "is_Mitigated"),
                    ("thread_id", "thread_id"),
                    ("mitigated", "mitigated"),
                    ("mitigated_by", "mitigated_by"),
                    ("reporter", "reporter"),
                    ("numerical_severity", "numerical_severity"),
                    ("last_reviewed", "last_reviewed"),
                    ("last_reviewed_by", "last_reviewed_by"),
                    ("line_number", "line_number"),
                    ("sourcefilepath", "sourcefilepath"),
                    ("sourcefile", "sourcefile"),
                    ("param", "param"),
                    ("payload", "payload"),
                    ("hash_code", "hash_code"),
                    ("line", "line"),
                    ("file_path", "file_path"),
                    ("static_finding", "static_finding"),
                    ("dynamic_finding", "dynamic_finding"),
                    ("created", "created"),
                    ("jira_creation", "jira_creation"),
                    ("jira_change", "jira_change"),
                    ("scanner_confidence", "scanner_confidence"),
                    ("sonarqube_issue", "sonarqube_issue"),
                    ("unique_id_from_tool", "unique_id_from_tool"),
                    ("sast_source_object", "sast_source_object"),
                    ("sast_sink_object", "sast_sink_object"),
                    ("sast_source_line", "sast_source_line"),
                    ("sast_source_file_path", "sast_source_file_path"),
                    ("nb_occurences", "nb_occurences"),
                ],
                max_length=200,
            ),
        ),
        migrations.AlterField(
            model_name="rule",
            name="match_field",
            field=models.CharField(
                choices=[
                    ("id", "id"),
                    ("title", "title"),
                    ("date", "date"),
                    ("cwe", "cwe"),
                    ("cve", "cve"),
                    ("url", "url"),
                    ("severity", "severity"),
                    ("description", "description"),
                    ("mitigation", "mitigation"),
                    ("impact", "impact"),
                    ("steps_to_reproduce", "steps_to_reproduce"),
                    ("severity_justification", "severity_justification"),
                    ("references", "references"),
                    ("test", "test"),
                    ("is_template", "is_template"),
                    ("active", "active"),
                    ("verified", "verified"),
                    ("false_p", "false_p"),
                    ("duplicate", "duplicate"),
                    ("duplicate_finding", "duplicate_finding"),
                    ("out_of_scope", "out_of_scope"),
                    ("under_review", "under_review"),
                    ("review_requested_by", "review_requested_by"),
                    ("under_defect_review", "under_defect_review"),
                    ("defect_review_requested_by", "defect_review_requested_by"),
                    ("is_Mitigated", "is_Mitigated"),
                    ("thread_id", "thread_id"),
                    ("mitigated", "mitigated"),
                    ("mitigated_by", "mitigated_by"),
                    ("reporter", "reporter"),
                    ("numerical_severity", "numerical_severity"),
                    ("last_reviewed", "last_reviewed"),
                    ("last_reviewed_by", "last_reviewed_by"),
                    ("line_number", "line_number"),
                    ("sourcefilepath", "sourcefilepath"),
                    ("sourcefile", "sourcefile"),
                    ("param", "param"),
                    ("payload", "payload"),
                    ("hash_code", "hash_code"),
                    ("line", "line"),
                    ("file_path", "file_path"),
                    ("static_finding", "static_finding"),
                    ("dynamic_finding", "dynamic_finding"),
                    ("created", "created"),
                    ("jira_creation", "jira_creation"),
                    ("jira_change", "jira_change"),
                    ("scanner_confidence", "scanner_confidence"),
                    ("sonarqube_issue", "sonarqube_issue"),
                    ("unique_id_from_tool", "unique_id_from_tool"),
                    ("sast_source_object", "sast_source_object"),
                    ("sast_sink_object", "sast_sink_object"),
                    ("sast_source_line", "sast_source_line"),
                    ("sast_source_file_path", "sast_source_file_path"),
                    ("nb_occurences", "nb_occurences"),
                ],
                max_length=200,
            ),
        ),
    ]
