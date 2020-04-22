# -*- coding: utf-8 -*-

import os
import unittest

from integraty.case import IntegraTestCase
from integraty.case import run_integra_tests
from integraty.extprog import ExternalProgram, ExternalProgramException

# To see this in action, just run with pytest from the root of the repository.
# $ pytest -v examples/simple1.py
"""
SimpleTestSuite is a class representing a suite (collection) of tests.
The organization is identical to how Python's unittest modules structures its
tests. Each method in the class starts with the `test_` prefix and is thought
to be a single test case. A single case does not necessarily mean there is only
one assertion, but it typically means that there is some behaviour which we are
making some assertions about, and we can perform multiple tests with the data
which we got back from the commands we ran.

Each method is meant to be private and not share any test details with other
methods. We want to isolate results of one test from being acted upon by
another test. It is possible to share state between test cases in the suite by
relying on class-level variables. The `get_class_var` method on the `self`
gives access to shared class-level state. Any variable name assigned in the
`setupClass` classmethod is accessible by passing that name as a string
argument to `get_class_var`. Do not be tempted to share mutable variables
between cases. If you are doing that to achieve some result, you are probably 
doing something that invalidates your tests.

As far as the organization of tests, there is no right or wrong here in terms
of whether each method only asserts a single thing or makes multiple assertions
about the data. It is worth keeping in mind that if some command takes a while
to run, it may make sense to run it just once and have multiple assertions in
the same method. Please, don't share results of a command via a class variable.
There be dragons if you do this.
"""


class SimpleTestSuite(IntegraTestCase):
    # All of these setup and teardown methods are completely optional. Remember,
    # `setUp` and `tearDown` run before and after EACH test method, while
    # `setUpClass` and `tearDownClass` run before all and after all test
    # methods.
    @classmethod
    def setUpClass(cls):
        # Here, we can setup anything that all other methods, aka test cases
        # will be able to access. It makes sense to share some read-only bits,
        # constants, etc., but do not attempt to mutate anything here.
        # This will run BEFORE all test methods.
        pass

    @classmethod
    def tearDownClass(cls):
        # Here we can teardown things if we set something up in the `setUpClass`
        # method above. This is unlikely to be used in itegration tests, but it
        # could be convenient in certain cases. This will run AFTER all the test
        # methods.
        pass

    def setUp(self):
        # Here we can setup anything that needs to be setup before each test
        # case. Be sure to undo whatever you do here in the `tearDown` method
        # below.
        pass

    def tearDown(self):
        # Here we undo what we did in `setUp` above.
        pass

    def test_example_printf(self):
        # Assign a command we intend to run to a variable, not required but
        # it makes it a little more obvious what our command is.
        cmd = 'printf "alpha beta gamma\ndelta epsilon zeta\n"'
        # Run the command with the ExternalProgram class as a context manager.
        # This is meant to be as low boilerplate as possible while still being
        # quite explicit about what we are actually doing.
        with ExternalProgram(cmd) as c:
            c.exec()
            # If we expect this subprocess call to succeed, we should check
            # that indeed the command ran successfully. It is possible to
            # provide a custom message via the `msg` argument to here if one
            # does not want to use default assertion failure message.
            self.assertCommandSucceeded(c)
            # At this point things are very open, but this is a good general
            # approach, where an expected and actual variables are assigned
            # and then used in assertions.
            expected = [('alpha', 'delta'), ('beta', 'epsilon'),
                        ('gamma', 'zeta')]
            actual = c.out.fields()
            self.assertListEqual(actual, expected)

    # Sometimes we actually want to mark a test as a known failure, perhaps it
    # is a temporary failure we are aware of, and we don't want it to appear in
    # results. The `@unittest.expectedFailure` decorator makes it easy to mark
    # a test as known broken.
    @unittest.expectedFailure
    def test_example_will_fail(self):
        cmd = 'not_a_real_printf "alpha beta gamma\ndelta epsilon zeta\n"'
        with ExternalProgram(cmd) as c:
            c.exec()
            self.assertCommandSucceeded(c)

    # Sometimes we want to conditionally skip tests. In this example we would
    # skip this test whenever we are running on MacOS X. On OSX the kernel
    # or `sysname` is `Darwin`.
    @unittest.skipIf(os.uname().sysname == 'Darwin', 'Sorry, no Darwins!')
    def test_example_no_osx(self):
        pass

    # On the other hand, we may want to skip unless the the condition is true.
    # In this example we would skip anywhere other than on OSX. There are other
    # decorators in the unittest module and they are well worth a look.
    # For Python3 have a look here, and adjust for the version you are running
    # from the dropdown there:
    # https://docs.python.org/3/library/unittest.html
    @unittest.skipUnless(os.uname().sysname == 'Darwin', 'Only Darwins!')
    def test_example_only_osx(self):
        pass

# This is just a little boilerplate, which lets us run this as an executable
# program.
if __name__ == "__main__":
    run_integra_tests(catchbreak=True)
