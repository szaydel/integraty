# -*- coding: utf-8 -*-

import re
import os
import sys

from integraty.case import IntegraTestCase
from integraty.case import run_integra_tests
from integraty.extprog import ExternalProgram, ExternalProgramException


class Similarity(IntegraTestCase):

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

    def test_domain_name_is_almost_equal(self):
        self.log.info("Tests string near equality assertions")
        cmd = self.get_class_var('dig_t_txt_microsoft_com')
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
                self.assertStringsAlmostEqualDiffLib(d['domain'],
                                                     'MicroS0ft.com',
                                                     ratio=0.74)


if __name__ == "__main__":
    run_integra_tests(catchbreak=True)
