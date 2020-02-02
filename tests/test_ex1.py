import os
import sys

from integraty.case import IntegraTestCase
from integraty.case import run_integra_tests
from integraty.extprog import ExternalProgram, ExternalProgramException
from integraty.productivity import TemporaryFile, ChecksumStream

class LibraryUsageEx1(IntegraTestCase):

    @classmethod
    def setUpClass(cls):
        # When we run in Travis-CI, we basically mock output of `whois` because
        # the command is not available on at least some test platforms.
        cls.whois_cloudflare_com_cmd = 'whois -h whois.cloudflare.com cloudflare.com'
        if os.getenv('TRAVIS', 'false') == 'true':
            p = os.path.join(os.path.dirname(__file__), 'whois_cloudflare_com')
            cls.whois_cloudflare_com_cmd = f'cat {p}'

        pass

    @classmethod
    def tearDownClass(cls):
        print("This will run after all tests in the class or on CTRL-C",
              file=sys.stderr)

    def test_domain_name_is_almost_equal(self):
        cmd = 'dig -t TXT microsoft.com'
        self.log.info("Tests string near equality assertions")
        with ExternalProgram(cmd) as c:
            c.exec()
            self.assertCommandSucceeded(c)
            list_of_dicts = c.out.to_dict_func(lambda l: zip(
                ('domain', '_', 'in', 'type', 'value'), l.split()),
                                               pattern='[; ]',
                                               exclude=True)
            for d in list_of_dicts:
                self.assertStringsAlmostEqual(d['domain'],
                                              'microsoft.com',
                                              ratio=0.75)
                self.assertStringsAlmostEqualCosine(d['domain'],
                                                    'MicroSoft.com',
                                                    ratio=0.5)

    def test_to_dict_mapping(self):

        def func(line: str) -> zip:
            if len(line.split()) < 2:
                return (None, None)
            tokens = line.split()
            return zip([tokens[4]], [tokens[0]])

        cmd = 'dig -x -t NS microsoft.com'
        self.log.info("Tests mapping function to dict translation")
        with ExternalProgram(cmd) as c:
            c.exec()
            self.assertCommandSucceeded(c)
            records = c.out.to_dict_func(func, pattern='[; ]', exclude=True)
            self.assertGreaterEqual(len(records), 5)

            # Ordering does not matter here, but this will break if number of
            # Nameservers changes. In other words, this could be an example of
            # a fairly fragile test.
            # This test will also break if any IP addresses change, but that's
            # perhaps what we want in this case.
            expected_keys = set([
                '13.77.161.179', '40.76.4.15', '13.77.161.179',
                '104.215.148.63', '40.113.200.201', '40.112.72.205'
            ])
            actual_keys = set([k for r in records for k, v in r.items()])
            self.assertSetEqual(expected_keys, actual_keys)

    def test_with_prefix(self):
        cmd = self.get_class_var('whois_cloudflare_com_cmd')
        self.log.info("Tests expected behaviour of with_prefix method")
        with ExternalProgram(cmd) as c:
            c.exec()
            self.assertCommandSucceeded(c)
            results = [
                ns.split(' ')[2] for ns in c.out.with_prefix(
                    'Name Server', sub_pattern=':', replacement='')
            ]
            # This is something of a smoke test example.
            self.assertGreaterEqual(len(results), 4)
            self.assertIn('ns3.cloudflare.com', results)
            self.assertIn('ns4.cloudflare.com', results)
            self.assertNotIn('ns8.cloudflare.com', results)
            self.assertNotIn('ns9.cloudflare.com', results)

    def test_with_suffix(self):
        cmd = self.get_class_var('whois_cloudflare_com_cmd')
        self.log.info("Tests expected behaviour of with_suffix method")
        with ExternalProgram(cmd) as c:
            c.exec()
            self.assertCommandSucceeded(c)
            results = [ns.split(':')[0] for ns in c.out.with_suffix('REDACTED')]
            # This is something of a smoke test example.
            self.assertGreaterEqual(len(results), 48)
            self.assertIn('Registrant Name', results)
            self.assertIn('Tech Country', results)
            self.assertIn('Tech Name', results)
            self.assertNotIn('Registrar', results)


if __name__ == "__main__":
    run_integra_tests(catchbreak=True)
