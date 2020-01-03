from case import IntegraTestCase
from case import run_integra_tests

import sys

class MyTest(IntegraTestCase):
    def test_1(self):
        self.shell('ls /tmp')
        # self.assertTrue(self.last_cmd_succeeded)
        self.shell('ls /var')
        # self.assertTrue(self.last_cmd_succeeded)
        self.shell('ls /usr')
        # self.assertTrue(self.last_cmd_succeeded)
        self.shell('ls /Users/szaydel')
        self.shell('/usr/bin/memory_pressure')
        print(self.stdout_line_tuples('/usr/bin/memory_pressure', strip_punct=True, strip_chars=r':,'), file=sys.stderr)
        self.assertEqual(
            self.stdout_lines_count(
                '/usr/bin/memory_pressure', pattern='Swap'), 3)
        # self.shell('ls /Users/szaydel1')

        # self.assertLastCommandIsOK()
        # self.assertLastCommandStdOutEqual('foobar')
        # self.assertLastCommandStdOutContains("Books and Courses!")
        self.assertAllCommandsAreOK()
        # print(self._cmd_results_list, file=sys.stderr)
        # self.shell('cat data.json')
        # print(self.json_loads('cat data.json'))
        # print(self.split_stdout('ls /usr'), file=sys.stderr)
        # print(self.split_stderr('ls /usr'), file=sys.stderr)
        # self.assertTrue(self.cmd_results('ls /tmp').ok)
        print(self.stdout_lines_with_prefix('/usr/bin/memory_pressure', 'Pages'), file=sys.stderr)

if __name__ == "__main__":
    run_integra_tests()