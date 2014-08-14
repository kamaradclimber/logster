from logster.parsers.RsyslogLogster import RsyslogLogster
import unittest


class TestRsyslogParser(unittest.TestCase):

    def test_whitelist_should_filter(self):
        whitelist = "--whitelist foo,bar"
        parser = RsyslogLogster(option_string=whitelist)
        lines = [
            "2014-08-14T09:10:42.716176+00:00 fc rsyslogd-pstats: foo: processed=0 failed=0",
            "2014-08-14T09:10:42.716177+00:00 fc rsyslogd-pstats: imudp(*:514): submitted=0",
            "2014-08-14T09:10:42.716178+00:00 fc rsyslogd-pstats: bar: submitted=0"
        ]
        for line in lines:
            parser.parse_line(line)

        names = set([k.split('.')[0] for k in parser.values.keys()])
        self.assertEquals(2, len(names))
        self.assertTrue('foo' in names)
        self.assertTrue('bar' in names)

    def test_empty_parseroptions_should_work(self):
        parser = RsyslogLogster(option_string="")
        line = "2014-08-14T09:10:42.716176+00:00 fc rsyslogd-pstats: foo: processed=0 failed=0"
        parser.parse_line(line)
        self.assertEqual(2, len(parser.values))
