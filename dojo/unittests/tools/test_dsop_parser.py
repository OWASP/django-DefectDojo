from os import path

from django.test import TestCase
from dojo.models import Test
from dojo.tools.dsop.parser import DsopParser


class TestDsopParser(TestCase):
    def test_zero_findings(self):
        testfile = open(path.join(path.dirname(__file__), "scans/dsop/zero_vuln.xlsx", "rb"))
        parser = DsopParser()
        findings = parser.get_findings(testfile, Test())
        self.assertEquals(len(findings), 0)

    def test_many_findings(self):
        testfile = open(path.join(path.dirname(__file__), "scans/dsop/many_vuln.xlsx", "rb"))
        parser = DsopParser()
        findings = parser.get_findings(testfile, Test())
        self.assertEquals(len(findings), 4)
        finding = findings[0]
        self.assertEqual("CVE-2019-15587", finding.cve)
        self.assertEqual("Low", finding.severity)
