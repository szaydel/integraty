# -*- coding: utf-8 -*-

import re
import os
import sys

from collections import ChainMap
from typing import NamedTuple

from integraty.case import IntegraTestCase
from integraty.case import run_integra_tests
from integraty.extprog import ExternalProgram, ExternalProgramException


class Functional(IntegraTestCase):

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

    def test_to_dict_mapping(self):
        self.log.info("Tests mapping function to dict translation")

        def func(line: str) -> zip:
            if len(line.split()) < 2:
                return (None, None)
            tokens = line.split()
            return zip([tokens[4]], [tokens[0]])

        cmd = self.get_class_var('dig_x_t_ns_microsoft_com')
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

    def test_filter_func(self):
        self.log.info("Tests expected behaviour of the filter method")
        cmd = self.get_class_var('whois_iana_org_home_arpa')
        with ExternalProgram(cmd) as c:
            c.exec()
            self.assertCommandSucceeded(c)
            results = c.out.filter_func(lambda l: re.search(
                r'\s(?:[0-9]{1,3}\.){3}[0-9]{1,3}\s', l))
            results_tuples = [tuple(elem.split()[1:3]) for elem in results]
            results_dict = {k.lower(): v for k, v in results_tuples}
            self.assertDictEqual(
                results_dict, {
                    'blackhole-1.iana.org': '192.175.48.6',
                    'blackhole-2.iana.org': '192.175.48.42'
                })

    def test_fold_funcs(self):
        self.log.info("Tests expected behaviour of the fold_funcs method")
        cmd = self.get_class_var('whois_iana_org_home_arpa')
        with ExternalProgram(cmd) as c:
            c.exec()
            self.assertCommandSucceeded(c)
            results = c.out.fold_funcs(
                # This may seem silly, because it is possible to combine them
                # into fewer expressions, but the goal here is to show how
                # function composition could be used to transform from input to
                # something we can make some sensible assertions about.
                lambda l: re.split(r'^.*:\s{0,}?(?=B)', l),
                lambda l: l[1].lower(),
                lambda l: l.split(),
                lambda l: {l[0]: l[2]},
                pattern='^nserver')
            self.assertListEqual(results,
                                 [{
                                     'blackhole-1.iana.org': '2620:4f:8000::6'
                                 }, {
                                     'blackhole-2.iana.org': '2620:4f:8000::42'
                                 }])

    def test_partial(self):
        self.log.info("Tests expected behaviour of the partial method")
        cmd = self.get_class_var('whois_iana_org_ip6_servers_arpa')

        def func(l, container):
            tokens = l.lower().split()
            return container(*tokens[1:4])

        class NameServer(NamedTuple):
            host: str
            ip_v4: str
            ip_v6: str

        with ExternalProgram(cmd) as c:
            c.exec()
            self.assertCommandSucceeded(c)
            results = c.out.partial(func, pattern='^nserver:')

            applied = [f(NameServer) for f in results if f]

            self.assertListEqual(applied, [
                NameServer(host='a.ip6-servers.arpa',
                           ip_v4='199.180.182.53',
                           ip_v6='2620:37:e000::53'),
                NameServer(host='b.ip6-servers.arpa',
                           ip_v4='199.253.182.182',
                           ip_v6='2001:500:86::86'),
                NameServer(host='c.ip6-servers.arpa',
                           ip_v4='196.216.169.11',
                           ip_v6='2001:43f8:110::11'),
                NameServer(host='d.ip6-servers.arpa',
                           ip_v4='200.7.86.53',
                           ip_v6='2001:13c7:7012::53'),
                NameServer(host='e.ip6-servers.arpa',
                           ip_v4='2001:dd8:6::101',
                           ip_v6='203.119.86.101'),
                NameServer(host='f.ip6-servers.arpa',
                           ip_v4='193.0.9.2',
                           ip_v6='2001:67c:e0::2')
            ])

    def test_map_func(self):
        self.log.info("Tests expected behaviour of the map_func method")
        cmd = self.get_class_var('whois_iana_org_home_arpa')
        with ExternalProgram(cmd) as c:
            c.exec()
            self.assertCommandSucceeded(c)
            results = c.out.map_func(func=lambda l: l.lower().split(),
                                     pattern='^domain')
            self.assertEqual(len(results), 1)
            self.assertListEqual(results[0], ['domain:', 'home.arpa'])
            results_dict = dict(zip(results[0], results[0][1:]))
            self.assertDictEqual(results_dict, {'domain:': 'home.arpa'})
            self.assertFalse(results_dict['domain:'] == 'HOME.ARPA')

    def test_filtered_map(self):
        self.log.info("Tests expected behaviour of the filtered_map method")
        cmd = self.get_class_var('whois_iana_org_home_arpa')

        def to_dict(l):
            """ Builds a nested dictionary """
            tokens = l.split()
            return {
                tokens[1].lower(): {
                    'v4_addr': tokens[2],
                    'v6_addr': tokens[3]
                }
            }

        with ExternalProgram(cmd) as c:
            c.exec()
            self.assertCommandSucceeded(c)
            results = c.out.filtered_map(
                filter_func=lambda l: l.startswith('nserver'),
                map_func=to_dict)
            results_dict = dict(ChainMap(*results))
            self.assertIn('blackhole-1.iana.org', results_dict)
            self.assertIn('blackhole-2.iana.org', results_dict)
            self.assertNotIn('blackhole-3.iana.org', results_dict)

    def test_groupby(self):
        self.log.info("Tests expected behaviour of the groupby method")
        cmd = self.get_class_var('whois_iana_org_ip6_servers_arpa')

        with ExternalProgram(cmd) as c:
            c.exec()
            self.assertCommandSucceeded(c)
            results_dict = c.out.groupby(
                lambda l: 'group A' if l.split()[1][0] <= 'C' else 'group B',
                pattern='nserver:')
            self.assertGreaterEqual(len(results_dict['group A']), 3)
            self.assertGreaterEqual(len(results_dict['group B']), 3)

            results_dict = c.out.groupby(
                lambda l: l.split(":", 1)[0],
                sub_pattern=r':\s{0,}?(?=[a-zA-Z0-9])',
                replacement=':',
                pattern=r'^%',
                exclude=True)
            groups = {
                k: [each.split(":", 1)[1] for each in v]
                for k, v in results_dict.items()
            }
            self.assertListEqual(groups['nserver'], [
                'A.IP6-SERVERS.ARPA 199.180.182.53 2620:37:e000::53',
                'B.IP6-SERVERS.ARPA 199.253.182.182 2001:500:86::86',
                'C.IP6-SERVERS.ARPA 196.216.169.11 2001:43f8:110::11',
                'D.IP6-SERVERS.ARPA 200.7.86.53 2001:13c7:7012::53',
                'E.IP6-SERVERS.ARPA 2001:dd8:6::101 203.119.86.101',
                'F.IP6-SERVERS.ARPA 193.0.9.2 2001:67c:e0::2'
            ])
            self.assertIn('IP6-SERVERS.ARPA', groups['domain'])
            self.assertIn('Los Angeles California 90094', groups['address'])
            self.assertIn('Reston Virginia 20190-5108', groups['address'])

    def test_groupby_count(self):
        self.log.info("Tests expected behaviour of the groupby_count method")
        cmd = self.get_class_var('whois_iana_org_ip6_servers_arpa')

        with ExternalProgram(cmd) as c:
            c.exec()
            self.assertCommandSucceeded(c)
            results_dict = c.out.groupby_count(
                lambda l: 'group A' if l.split()[1][0] \
                    <= 'C' else 'group B',
                pattern='nserver:')
            self.assertEqual(results_dict['group A'], 3)
            self.assertEqual(results_dict['group B'], 3)

            results_dict = c.out.groupby_count(lambda l: l.split()[1],
                                               pattern='nserver:')
            self.assertEqual(results_dict['A.IP6-SERVERS.ARPA'], 1)
            self.assertEqual(results_dict['E.IP6-SERVERS.ARPA'], 1)

            results_dict = c.out.groupby_count(lambda l: l.split()[0][:-1],
                                               pattern='organisation|address')
            self.assertEqual(results_dict['organisation'], 3)
            self.assertEqual(results_dict['address'], 14)


if __name__ == "__main__":
    run_integra_tests(catchbreak=True)
