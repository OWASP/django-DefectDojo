import json
import re

from dojo.models import Finding

__author__ = "Roy Shoemake"
__status__ = "Development"


# Function to remove HTML tags
TAG_RE = re.compile(r'<[^>]+>')


def cleantags(text=''):
    prepared_text = text if text else ''
    return TAG_RE.sub('', prepared_text)


class NetsparkerParser(object):

    def get_scan_types(self):
        return ["Netsparker Scan"]

    def get_label_for_scan_types(self, scan_type):
        return "Netsparker Scan"

    def get_description_for_scan_types(self, scan_type):
        return "Netsparker JSON format."

    def get_findings(self, filename, test):
        tree = filename.read()
        try:
            data = json.loads(str(tree, 'utf-8-sig'))
        except:
            data = json.loads(tree)
        dupes = dict()

        for item in data["Vulnerabilities"]:
            categories = ''
            language = ''
            mitigation = ''
            impact = ''
            references = ''
            findingdetail = ''
            title = ''
            group = ''
            status = ''

            title = item["Name"]
            findingdetail = cleantags(item["Description"])
            cwe = item["Classification"]["Cwe"] if "Cwe" in item["Classification"] else None
            sev = item["Severity"]
            if sev not in ['Info', 'Low', 'Medium', 'High', 'Critical']:
                sev = 'Info'
            mitigation = cleantags(item["RemedialProcedure"])
            references = cleantags(item["RemedyReferences"])
            url = item["Url"]
            impact = cleantags(item["Impact"])
            dupe_key = title + item["Name"] + item["Url"]

            if dupe_key in dupes:
                find = dupes[dupe_key]
            else:
                dupes[dupe_key] = True

                find = Finding(title=title,
                               test=test,
                               description=findingdetail,
                               severity=sev.title(),
                               mitigation=mitigation,
                               impact=impact,
                               references=references,
                               url=url,
                               cwe=cwe,
                               static_finding=True)
                dupes[dupe_key] = find
                findingdetail = ''

        return list(dupes.values())
