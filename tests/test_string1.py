# -*- coding: utf-8 -*-

import re
import os
import sys

from itertools import chain

from integraty.case import IntegraTestCase
from integraty.case import run_integra_tests
from integraty.extprog import ExternalProgram, ExternalProgramException
from integraty.productivity import TemporaryFile, ChecksumStream


class String1(IntegraTestCase):

    @classmethod
    def setUpClass(cls):
        # When we run in Travis-CI, we basically mock output of `whois` because
        # the command is not available on at least some test platforms.
        cls.whois_cloudflare_com = 'whois -h whois.cloudflare.com cloudflare.com'
        cls.whois_iana_org_azure = 'whois -h whois.iana.org .azure'
        cls.whois_iana_org_home_arpa = 'whois -h whois.iana.org home.arpa'
        cls.whois_iana_org_ip6_servers_arpa = 'whois -h whois.iana.org ip6-servers.arpa'
        cls.whois_iana_org_ip6_arpa = 'whois -h whois.iana.org ip6.arpa'
        cls.host_t_mx_cloudflare_com = 'host -t MX cloudflare.com'
        cls.host_t_mx_googlemail_com = 'host -t MX googlemail.com'
        cls.host_t_aaaa_cloudflare_com = 'host -t AAAA cloudflare.com'
        cls.dig_t_txt_microsoft_com = 'dig -t TXT microsoft.com'
        cls.dig_x_t_ns_microsoft_com = 'dig -x -t NS microsoft.com'
        cls.dig_t_aaaa_cloudflare_com = 'dig -t AAAA cloudflare.com'
        cls.dig_t_mx_cloudflare_com = 'dig -t MX cloudflare.com'
        if any([os.getenv('TRAVIS', 'false'), os.getenv('CIRCLECI', 'false')]):
            for elem in [
                    'whois_cloudflare_com',
                    'whois_iana_org_azure',
                    'whois_iana_org_home_arpa',
                    'whois_iana_org_ip6_servers_arpa',
                    'whois_iana_org_ip6_arpa',
                    'host_t_mx_cloudflare_com',
                    'host_t_mx_googlemail_com',
                    'host_t_aaaa_cloudflare_com',
                    'dig_t_txt_microsoft_com',
                    'dig_x_t_ns_microsoft_com',
                    'dig_t_aaaa_cloudflare_com',
                    'dig_t_mx_cloudflare_com',
            ]:
                setattr(
                    cls, f'{elem}',
                    f'cat {os.path.join(os.path.dirname(__file__), elem)}')

    @classmethod
    def tearDownClass(cls):
        print("This will run after all tests in the class or on CTRL-C",
              file=sys.stderr)

    def test_with_prefix(self):
        self.log.info("Tests expected behaviour of with_prefix method")
        cmd = self.get_class_var('whois_cloudflare_com')
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
        self.log.info("Tests expected behaviour of the with_suffix method")
        cmd = self.get_class_var('whois_cloudflare_com')
        with ExternalProgram(cmd) as c:
            c.exec()
            self.assertCommandSucceeded(c)
            results = [
                ns.split(':')[0] for ns in c.out.with_suffix('REDACTED')
            ]
            # This is something of a smoke test example.
            self.assertGreaterEqual(len(results), 48)
            self.assertIn('Registrant Name', results)
            self.assertIn('Tech Country', results)
            self.assertIn('Tech Name', results)
            self.assertNotIn('Registrar', results)

    def test_trim_prefix(self):
        self.log.info("Tests expected behaviour of trim_prefix method")
        cmd = self.get_class_var('whois_iana_org_ip6_arpa')
        with ExternalProgram(cmd) as c:
            c.exec()
            self.assertCommandSucceeded(c)
            results = [
                ns.split(maxsplit=2)
                for ns in c.out.trim_prefix('nserver:      ',
                                            pattern='nserver')
            ]
            results_dict = {l[0].lower(): tuple(l[1:]) for l in results}
            self.assertGreaterEqual(len(results), 6)
            self.assertIn('a.ip6-servers.arpa', results_dict)
            self.assertIn('e.ip6-servers.arpa', results_dict)
            self.assertNotIn('h.ip6-servers.arpa', results_dict)
            self.assertNotIn('k.ip6-servers.arpa', results_dict)
            self.assertTupleEqual(results_dict['d.ip6-servers.arpa'],
                                  ('200.7.86.53', '2001:13c7:7012::53'))
            self.assertTupleEqual(results_dict['b.ip6-servers.arpa'],
                                  ('199.253.182.182', '2001:500:86::86'))

    def test_lastn(self):
        self.log.info("Tests expected behaviour of lastn method")
        cmd = self.get_class_var('whois_iana_org_ip6_arpa')
        with ExternalProgram(cmd) as c:
            c.exec()
            self.assertCommandSucceeded(c)
            results_pairs = [
                line.split() for line in c.out.lastn(
                    3, sub_pattern=r':\s{0,}', replacement=' ')
            ]
            results_dict = {k: v for k, v in results_pairs}
            self.assertEqual(len(results_pairs), 3)
            self.assertDictEqual(results_dict, {
                'created': '2001-11-10',
                'changed': '2018-11-13',
                'source': 'IANA'
            })

    def test_firstn(self):
        self.log.info("Tests expected behaviour of firstn method")
        cmd = self.get_class_var('whois_iana_org_ip6_arpa')
        with ExternalProgram(cmd) as c:
            c.exec()
            self.assertCommandSucceeded(c)
            results_pairs = [
                line.split(maxsplit=1)
                for line in c.out.firstn(2,
                                         sub_pattern=r':\s{0,}',
                                         replacement=' ',
                                         pattern='(^[% ] | ^$)',
                                         exclude=True)
            ]
            results_dict = {k: v for k, v in results_pairs}
            self.assertEqual(len(results_pairs), 2)
            self.assertDictEqual(
                results_dict, {
                    'domain': 'IP6.ARPA',
                    'organisation': 'Internet Architecture Board (IAB)'
                })

    def test_line_tuples(self):
        self.log.info("Tests expected behaviour of the line_tuples method")
        cmd = self.get_class_var('host_t_mx_googlemail_com')
        with ExternalProgram(cmd) as c:
            c.exec()
            self.assertCommandSucceeded(c)
            results = c.out.line_tuples(pattern='^;', exclude=True)
            results_dict = dict(
                zip((i[5] for i in results), (i[6] for i in results)))
            self.assertSetEqual(set(results_dict.keys()),
                                set(['5', '10', '20', '30', '40']))
            self.assertDictEqual(
                results_dict, {
                    '10': 'alt1.gmail-smtp-in.l.google.com.',
                    '20': 'alt2.gmail-smtp-in.l.google.com.',
                    '30': 'alt3.gmail-smtp-in.l.google.com.',
                    '40': 'alt4.gmail-smtp-in.l.google.com.',
                    '5': 'gmail-smtp-in.l.google.com.'
                })
            # Order no longer matters...
            self.assertDictEqual(
                results_dict, {
                    '5': 'gmail-smtp-in.l.google.com.',
                    '40': 'alt4.gmail-smtp-in.l.google.com.',
                    '20': 'alt2.gmail-smtp-in.l.google.com.',
                    '10': 'alt1.gmail-smtp-in.l.google.com.',
                    '30': 'alt3.gmail-smtp-in.l.google.com.',
                })
        cmd = self.get_class_var('whois_iana_org_azure')
        with ExternalProgram(cmd) as c:
            c.exec()
            self.assertCommandSucceeded(c)
            results = c.out.line_tuples(sep=r':\s+',
                                        maxsplit=1,
                                        pattern='^org|^domain')
            self.assertIn(('organisation', 'Microsoft Corporation'), results)
            self.assertIn(('organisation', 'Verisign, Inc'), results)
            self.assertIn(('domain', 'AZURE'), results)
            results_dict = dict(results)
            self.assertDictEqual(results_dict, {
                'domain': 'AZURE',
                'organisation': 'Verisign, Inc'
            })

    def test_fields(self):
        self.log.info("Tests expected behaviour of the fields method")
        cmd = self.get_class_var('whois_cloudflare_com')
        with ExternalProgram(cmd) as c:
            c.exec()
            self.assertCommandSucceeded(c)
            domain_name, = c.out.fields(pattern='Domain Name')[2]
            registrar_url, = c.out.fields(pattern='Registrar URL')[2]
            self.assertEqual(domain_name.lower(), 'cloudflare.com')
            self.assertEqual(registrar_url, 'https://www.cloudflare.com')

        cmd = self.get_class_var('dig_t_aaaa_cloudflare_com')
        with ExternalProgram(cmd) as c:
            c.exec()
            self.assertCommandSucceeded(c)
            results = c.out.fields(pattern='[;]', exclude=True)
            self.assertDictEqual(
                dict(zip(results[4], results[0])), {
                    '2606:4700::6811:af55': 'cloudflare.com.',
                    '2606:4700::6811:b055': 'cloudflare.com.'
                })

    def test_take_column(self):
        self.log.info("Tests expected behaviour of the take_column method")
        cmd = self.get_class_var('host_t_aaaa_cloudflare_com')
        with ExternalProgram(cmd) as c:
            c.exec()
            self.assertCommandSucceeded(c)

            # One approach could be to take two columns with two separate calls
            # and zip them together to build dicts.
            results_values = c.out.take_column(column=0)
            results_keys = c.out.take_column(column=4)
            self.assertDictEqual(
                dict(zip(results_keys, results_values)), {
                    '2606:4700::6811:af55': 'cloudflare.com',
                    '2606:4700::6811:b055': 'cloudflare.com'
                })
            results = c.out.take_column(column=4)
            # This is arguably fragile as well, because over time these may
            # change, or new quad records may get added.
            self.assertSetEqual(
                set(results),
                set(['2606:4700::6811:af55', '2606:4700::6811:b055']))
            # A better test may be to see if we are finding quad records, or
            # if we are certain at least these two particular addresses must
            # exist, we can assert their presence in the sequence like so.
            self.assertIn('2606:4700::6811:af55', results)
            self.assertIn('2606:4700::6811:b055', results)

        cmd = self.get_class_var('host_t_mx_cloudflare_com')
        with ExternalProgram(cmd) as c:
            c.exec()
            self.assertCommandSucceeded(c)
            results = c.out.take_column(column=6)
            self.assertSetEqual(
                set(results),
                set([
                    'aspmx.l.google.com.', 'alt1.aspmx.l.google.com.',
                    'alt2.aspmx.l.google.com.', 'aspmx2.googlemail.com.',
                    'aspmx3.googlemail.com.'
                ]))

    def test_compress(self):
        self.log.info("Tests expected behaviour of the compress method")
        cmd = self.get_class_var('dig_t_mx_cloudflare_com')
        with ExternalProgram(cmd) as c:
            c.exec()
            self.assertCommandSucceeded(c)
            results = c.out.compress(indexes=(0, 5),
                                     pattern='[;]',
                                     exclude=True)
            # This is also an example of a fairly fragile test, because these
            # types of information may be volatile. It may be better to test
            # if one or more stable values are present in the results, or that
            # results is not empty.
            self.assertSetEqual(
                set(results),
                set([('cloudflare.com.', 'aspmx.l.google.com.'),
                     ('cloudflare.com.', 'alt1.aspmx.l.google.com.'),
                     ('cloudflare.com.', 'alt2.aspmx.l.google.com.'),
                     ('cloudflare.com.', 'aspmx2.googlemail.com.'),
                     ('cloudflare.com.', 'aspmx3.googlemail.com.')]))
            self.assertCountEqual(
                results, [('cloudflare.com.', 'aspmx.l.google.com.'),
                          ('cloudflare.com.', 'alt1.aspmx.l.google.com.'),
                          ('cloudflare.com.', 'alt2.aspmx.l.google.com.'),
                          ('cloudflare.com.', 'aspmx2.googlemail.com.'),
                          ('cloudflare.com.', 'aspmx3.googlemail.com.')])

    def test_take_range_fields(self):
        self.log.info(
            "Tests expected behaviour of the take_range_fields method")
        cmd = self.get_class_var('whois_iana_org_home_arpa')
        with ExternalProgram(cmd) as c:
            c.exec()
            self.assertCommandSucceeded(c)
            results = c.out.take_range_fields(
                sep=r'^.*:\s{0,}?(?=[a-zA-Z0-9])',
                slc_range=(0, 2),
                pattern='address')
            self.assertEqual(
                " ".join(chain(*results[:5])),
                'c/o IETF Administrative Support Activity, ISOC 1775 Wiehle Ave. Suite 102 Reston Virginia 20190-5108 United States'
            )


if __name__ == "__main__":
    run_integra_tests(catchbreak=True)
