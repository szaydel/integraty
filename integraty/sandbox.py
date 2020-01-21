from case import IntegraTestCase
from case import run_integra_tests
from extprog import ExternalProgram, ExternalProgramException
from productivity import TemporaryFile, ChecksumStream

import sys

class MyTest(IntegraTestCase):
    @classmethod
    def setUpClass(cls):
        cls.shared_var = 'shared variable'
        pass

    def test_1(self):
        print(self.get_class_var('shared_var'), file=sys.stderr)
        # self.log.debug("This is low level stuff")
        # self.log.info("This is info")
        # self.log.error("This is error")

        # c = ExternalProgram('integraty/command')
        with ExternalProgram('integraty/command') as c:
            c.do_shell()
            res = c.stdout_to_dict_func(lambda l: (l.split()[0], l.split()[1]))
            self.log.info(res)
        # res = c.stdout_dict_from_line(keys=["xx", "yy", "zz", "a", "b", "c", "d", "e", "f"], pattern="Foo")
        # res = c.stdout_lines(skip_head=2, skip_tail=300)

        # res = c.stdout_to_dict_map_func(lambda x: x.split()[0:2])
        # res = c.stdout_columns(pattern="Foobar")
        # res = c.stdout_filter_func(lambda l: l.startswith('1'))
        # res = c.stdout_line_tuples(pattern="Foobar", exclude=True)
        # res = c.stdout_map_func(lambda l: dict(zip(*tuple(l.split()[0:2]))))
        # res = c.stdout_map_func(lambda l: (l.split()[0], l.split()[2]))
        # res = c.stdout_funcs_pipeline(lambda v: v.split()[1], lambda v: v.lower(), lambda v: v.capitalize())
        # self.log.info(res)
        # print(c.out, file=sys.stderr)
        # print(c.stdout_lines(pattern=".apple."), file=sys.stderr)
        # print(c.stdout_lines_with_prefix(prefix="com.", exclude=True), file=sys.stderr)
        # res = c.stdout_take_column(column=0, pattern="Foobar")
        # res = c.stdout_take_some_columns(selectors=(2,), pattern="Foobar")
        # res = c.stdout_with_prefix(prefix="1")
        # res = c.stdout_to_tuple_func(lambda l: (l.split()[0], l.split()[1], l.split()[2]))
        
        # res = c.stdout_tail(pattern="Foobar")
        # res = c._trim_prefix('1 ')
        # res = c._trim_suffix('delta')
        # print(c.stdout_map_func(func=lambda l: l.upper()), file=sys.stderr)
        # print(c.stdout_take_range_columns(slc_range=(1,3), pattern="Foobar"), file=sys.stderr)
        # print(c.stdout_take_some_columns(selectors=[True, True, True], pattern="Foobar"), file=sys.stderr)
        # print(c.stdout_head(), file=sys.stderr)
        # print(c.stdout_tail(), file=sys.stderr)
        # print(c.stdout_dict_from_line(), file=sys.stderr)
        # print(c.stdout_dict_from_line(keys=('a', 'b', 'c')), file=sys.stderr)
        # print(c.stdout_firstn(n=-1000), file=sys.stderr)
        # print(c.stdout_dict_transform_func(lambda x: (x.split()[1], int(x.split()[0]))), file=sys.stderr)
        # print(c.stdout_trim_prefix('1'), file=sys.stderr)
        # print(c.stdout_trim_suffix('epsilon'), file=sys.stderr)
        # print(c.stdout_lastn(n=3), file=sys.stderr)
        # self.assertNoStderr(c)
        # print(c.out, file=sys.stderr)
        # self.assertCommandSucceeded(c)
        # print(c, file=sys.stderr)
        # self.run('ls /tmp')
        # self.assertTrue(self.last_cmd_succeeded)
        # self.run('ls /var')
        # self.assertTrue(self.last_cmd_succeeded)
        # self.run('ls /usr')
        # self.assertTrue(self.last_cmd_succeeded)
        # self.run('ls /Users/szaydel')
        # self.run('/usr/bin/memory_pressure')
        # print(self.stdout_line_tuples('/usr/bin/memory_pressure', strip_punct=True, strip_chars=r':,'), file=sys.stderr)
        # self.assertEqual(
            # self.stdout_lines_count(
                # '/usr/bin/memory_pressure', pattern='Swap'), 3)
        # self.run('ls /Users/szaydel1')

        # self.assertLastCommandIsOK()
        # self.assertLastCommandStdOutEqual('foobar')
        # self.assertLastCommandStdOutContains("Books and Courses!")
        # self.assertAllCommandsAreOK()
        # print(self._cmd_results_list, file=sys.stderr)
        # self.run('cat data.json')
        # print(self.json_loads('cat data.json'))
        # print(self.split_stdout('ls /usr'), file=sys.stderr)
        # print(self.split_stderr('ls /usr'), file=sys.stderr)
        # self.assertTrue(self.cmd_results('ls /tmp').ok)
        # print(self.stdout_lines_with_prefix('/usr/bin/memory_pressure', 'Pages'), file=sys.stderr)
        # self.log.info("Checking if data.json1 exists")
        # self.assertFileModifiedAfter("data.json", 1)
        # self.assertFileSHA256Equals("data.json", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")

        # t = TemporaryFile(virtual=False)
        # t.write(b'FooBaXXrBaz')
        # self.log.info(t.abspath)
        # self.log.info(ChecksumStream(open('data.enc', 'r+b')).base64_dec)
        # self.log.info(ChecksumStream(open('data.json', 'r+b')).base64_enc)

        # self.log.info(f"Checksum: {ChecksumFile('data.json').sha256}")

if __name__ == "__main__":
    run_integra_tests()