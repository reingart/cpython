"""Test cases for traceback module"""

import unittest
from test.test_support import run_unittest, is_jython

import traceback

class TbError(Exception):
    pass

class TracebackCases(unittest.TestCase):
    # For now, a very minimal set of tests.  I want to be sure that
    # formatting of SyntaxErrors works based on changes for 2.1.

    def get_exception_format(self, func, exc):
        try:
            func()
        except exc, value:
            return traceback.format_exception_only(exc, value)
        else:
            raise ValueError, "call did not raise exception"

    def syntax_error_with_caret(self):
        compile("def fact(x):\n\treturn x!\n", "?", "exec")

    def syntax_error_without_caret(self):
        # XXX why doesn't compile raise the same traceback?
        import test.badsyntax_nocaret

    def syntax_error_bad_indentation(self):
        compile("def spam():\n  print 1\n print 2", "?", "exec")

    def test_caret(self):
        err = self.get_exception_format(self.syntax_error_with_caret,
                                        SyntaxError)
        self.assert_(len(err) == 4)
        self.assert_("^" in err[2]) # third line has caret
        self.assert_(err[1].strip() == "return x!")

    def test_nocaret(self):
        if is_jython:
            # jython adds a caret in this case (why shouldn't it?)
            return
        err = self.get_exception_format(self.syntax_error_without_caret,
                                        SyntaxError)
        self.assert_(len(err) == 3)
        self.assert_(err[1].strip() == "[x for x in x] = x")

    def test_bad_indentation(self):
        err = self.get_exception_format(self.syntax_error_bad_indentation,
                                        IndentationError)
        self.assert_(len(err) == 4)
        self.assert_("^" in err[2])
        self.assert_(err[1].strip() == "print 2")

    def test_bug737473(self):
        import sys, os, tempfile, time

        savedpath = sys.path[:]
        testdir = tempfile.mkdtemp()
        try:
            sys.path.insert(0, testdir)
            testfile = os.path.join(testdir, 'test_bug737473.py')
            print >> open(testfile, 'w'), """
def test():
    raise ValueError"""

            if 'test_bug737473' in sys.modules:
                del sys.modules['test_bug737473']
            import test_bug737473

            try:
                test_bug737473.test()
            except ValueError:
                # this loads source code to linecache
                traceback.extract_tb(sys.exc_traceback)

            # If this test runs too quickly, test_bug737473.py's mtime
            # attribute will remain unchanged even if the file is rewritten.
            # Consequently, the file would not reload.  So, added a sleep()
            # delay to assure that a new, distinct timestamp is written.
            # Since WinME with FAT32 has multisecond resolution, more than
            # three seconds are needed for this test to pass reliably :-(
            time.sleep(4)

            print >> open(testfile, 'w'), """
def test():
    raise NotImplementedError"""
            reload(test_bug737473)
            try:
                test_bug737473.test()
            except NotImplementedError:
                src = traceback.extract_tb(sys.exc_traceback)[-1][-1]
                self.failUnlessEqual(src, 'raise NotImplementedError')
        finally:
            sys.path[:] = savedpath
            for f in os.listdir(testdir):
                os.unlink(os.path.join(testdir, f))
            os.rmdir(testdir)

    def test_members(self):
        # Covers Python/structmember.c::listmembers()
        try:
            1/0
        except:
            import sys
            sys.exc_traceback.__members__

    def raise_tberror(self):
        raise TbError

    def raise_typeerror(self):
        raise TypeError

    def test_modulename(self):
        # Bug 860326: format_exception_only should prepend module name
        # to exceptions not in "exceptions", like PyErr_Print does.
        err = self.get_exception_format(self.raise_tberror, TbError)
        self.assertEquals(len(err), 1)
        self.assert_(err[0] == '__main__.TbError\n' or
                     err[0] == 'test.test_traceback.TbError\n')

        err = self.get_exception_format(self.raise_typeerror, TypeError)
        self.assertEquals(err[0], 'TypeError\n')


def test_main():
    run_unittest(TracebackCases)


if __name__ == "__main__":
    test_main()
