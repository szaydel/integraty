from integraty.case import IntegraTestCase
from integraty.case import run_integra_tests
from integraty.extprog import ExternalProgram, ExternalProgramException
from integraty.productivity import TemporaryFile, ChecksumStream

import sys


class MyTest(IntegraTestCase):

    @classmethod
    def setUpClass(cls):
        cls.shared_var = 'shared variable'
        pass

    @classmethod
    def tearDownClass(cls):
        print("Tearing down...", file=sys.stderr)

    def test_1(self):
        print(self.get_class_var('shared_var'), file=sys.stderr)
        # self.log.debug("This is low level stuff")
        # self.log.info("This is info")
        # self.log.error("This is error")

        # c = ExternalProgram('integraty/command')
        with ExternalProgram('integraty/command') as c:
            c.exec()
            # res = c.fold_funcs(lambda l: l.split(), lambda l: len(l), lambda l: l*3)
            res = c.out.to_dict_func(lambda l: (l.split()[0], l.split()[1]))
            # res = c.compress(indexes=(0,1,2), pattern="Foobar")
            # res = c.out.pairs()
            self.log.info(res)
            # res = c.pairs(as_dict=True)
            # self.log.info(res)
            # res = c.groupby(column=1)
            # res = c.out.compress(indexes=(1, 2))
            res = c.out.skip_lines(skip_head=1, pattern="alpha")
            self.log.info(res)
        # res = c.dict_from_line(keys=["xx", "yy", "zz", "a", "b", "c", "d", "e", "f"], pattern="Foo")
        # res = c.lines(skip_head=2, skip_tail=300)

        # res = c.to_dict_map_func(lambda x: x.split()[0:2])
        # res = c.columns(pattern="Foobar")
        # res = c.filter_func(lambda l: l.startswith('1'))
        # res = c.line_tuples(pattern="Foobar", exclude=True)
        # res = c.map_func(lambda l: dict(zip(*tuple(l.split()[0:2]))))
        # res = c.map_func(lambda l: (l.split()[0], l.split()[2]))
        # res = c.funcs_pipeline(lambda v: v.split()[1], lambda v: v.lower(), lambda v: v.capitalize())
        # self.log.info(res)
        # print(c.out, file=sys.stderr)
        # print(c.lines(pattern=".apple."), file=sys.stderr)
        # print(c.lines_with_prefix(prefix="com.", exclude=True), file=sys.stderr)
        # res = c.take_column(column=0, pattern="Foobar")
        # res = c.with_prefix(prefix="1")
        # res = c.to_tuple_func(lambda l: (l.split()[0], l.split()[1], l.split()[2]))

        # res = c.tail(pattern="Foobar")
        # res = c._trim_prefix('1 ')
        # res = c._trim_suffix('delta')
        # print(c.map_func(func=lambda l: l.upper()), file=sys.stderr)
        # print(c.take_range_columns(slc_range=(1,3), pattern="Foobar"), file=sys.stderr)
        # print(c.take_some_columns(selectors=[True, True, True], pattern="Foobar"), file=sys.stderr)
        # print(c.head(), file=sys.stderr)
        # print(c.tail(), file=sys.stderr)
        # print(c.dict_from_line(), file=sys.stderr)
        # print(c.dict_from_line(keys=('a', 'b', 'c')), file=sys.stderr)
        # print(c.firstn(n=-1000), file=sys.stderr)
        # print(c.dict_transform_func(lambda x: (x.split()[1], int(x.split()[0]))), file=sys.stderr)
        # print(c.trim_prefix('1'), file=sys.stderr)
        # print(c.trim_suffix('epsilon'), file=sys.stderr)
        # print(c.lastn(n=3), file=sys.stderr)
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
        # print(self.line_tuples('/usr/bin/memory_pressure', strip_punct=True, strip_chars=r':,'), file=sys.stderr)
        # self.assertEqual(
        # self.lines_count(
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
        # print(self.lines_with_prefix('/usr/bin/memory_pressure', 'Pages'), file=sys.stderr)
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
    run_integra_tests(catchbreak=True)
