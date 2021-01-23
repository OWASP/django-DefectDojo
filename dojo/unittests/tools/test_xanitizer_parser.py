from django.test import TestCase
from dojo.tools.xanitizer.parser import XanitizerXMLParser
from dojo.models import Engagement, Product, Test


class TestXanitizerXMLParser(TestCase):

    def test_parse_without_file_has_no_findings(self):
        parser = XanitizerXMLParser()
        findings = parser.get_findings(None, Test())
        self.assertEqual(0, len(findings))

    def test_parse_file_with_no_findings(self):
        testfile = open("dojo/unittests/scans/xanitizer/no-findings.xml")
        parser = XanitizerXMLParser()
        findings = parser.get_findings(testfile, Test())
        self.assertEqual(0, len(findings))

    def test_parse_file_with_one_findings(self):
        testfile = open("dojo/unittests/scans/xanitizer/one-findings.xml")
        parser = XanitizerXMLParser()
        findings = parser.get_findings(testfile, Test())
        self.assertEqual(1, len(findings))

    def test_parse_file_with_multiple_findings(self):
        testfile = open("dojo/unittests/scans/xanitizer/multiple-findings.xml")
        parser = XanitizerXMLParser()
        findings = parser.get_findings(testfile, Test())
        self.assertEqual(9, len(findings))

    def test_parse_file_with_multiple_findings_no_details(self):
        testfile = open("dojo/unittests/scans/xanitizer/multiple-findings-no-details.xml")
        parser = XanitizerXMLParser()
        findings = parser.get_findings(testfile, Test())
        self.assertEqual(9, len(findings))
