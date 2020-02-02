from integraty.case import IntegraTestCase
from integraty.case import run_integra_tests
from integraty.extprog import ExternalProgram, ExternalProgramException
from integraty.productivity import TemporaryFile, ChecksumStream

import sys


class MyTest(IntegraTestCase):

    @classmethod
    def setUpClass(cls):
        cls.cmd = 'dig -t TXT microsoft.com'
        pass

    @classmethod
    def tearDownClass(cls):
        print("This will run after all tests in the class or on CTRL-C",
              file=sys.stderr)

    def test_domain_name_is_almost_equal(self):
        self.log.info(f"Calling: {self.get_class_var('cmd')}")
        with ExternalProgram(self.get_class_var('cmd')) as c:
            c.exec()
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


if __name__ == "__main__":
    run_integra_tests(catchbreak=True)
