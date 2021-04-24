from os import path

from django.test import TestCase
from dojo.models import Test
from dojo.tools.huskyci.parser import HuskyCIParser


class TestHuskyCIParser(TestCase):

    def test_parse_file_no_finding(self):
        testfile = open(path.join(path.dirname(__file__), "scans/huskyci/huskyci_report_no_finding.json"))
        parser = HuskyCIParser()
        findings = parser.get_findings(testfile, Test())
        self.assertEqual(0, len(findings))

    def test_parse_file_has_one_finding_one_tool(self):
        testfile = open(
            path.join(path.dirname(__file__), "scans/huskyci/huskyci_report_one_finding_one_tool.json")
        )
        parser = HuskyCIParser()
        findings = parser.get_findings(testfile, Test())
        testfile.close()
        self.assertEqual(1, len(findings))

    def test_parse_file_has_many_finding_one_tool(self):
        testfile = open(
            path.join(path.dirname(__file__), "scans/huskyci/huskyci_report_many_finding_one_tool.json")
        )
        parser = HuskyCIParser()
        findings = parser.get_findings(testfile, Test())
        testfile.close()
        self.assertEqual(3, len(findings))

    def test_parse_file_has_many_finding_two_tools(self):
        testfile = open(
            path.join(path.dirname(__file__), "scans/huskyci/huskyci_report_many_finding_two_tools.json")
        )
        parser = HuskyCIParser()
        findings = parser.get_findings(testfile, Test())
        testfile.close()
        self.assertEqual(15, len(findings))
