# -------------------------------------------------------------------------------
#
#  Copyright (c) 2018 Waysys LLC
#
# -------------------------------------------------------------------------------
#
#  Waysys LLC MAKES NO REPRESENTATIONS OR WARRANTIES ABOUT THE SUITABILITY OF
#  THE SOFTWARE, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
#  TO THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#  PARTICULAR PURPOSE, OR NON-INFRINGEMENT. CastleBay SHALL NOT BE LIABLE FOR
#  ANY DAMAGES SUFFERED BY LICENSEE AS A RESULT OF USING, MODIFYING OR
#  DISTRIBUTING THIS SOFTWARE OR ITS DERIVATIVES.
#
# For further information, contact wshaffer@waysysweb.com
#
# -------------------------------------------------------------------------------

__author__ = 'Bill Shaffer'
__version__ = "31-Dec-2020"

"""
This module holds the FileBuilder class. 
"""

from suitedreamsexception import SuiteDreamsException
from testcase import TestCase

# -------------------------------------------------------------------------------
#  FileBuilder class
# -------------------------------------------------------------------------------


class FileBuilder:
    """
    The File Builder class creates a single test case file in HTML format.  It is the
    intermediate between the main module, the product specification, and the test case.
    The main role of this class is to handle the input/output for the test case.
    """

    def __init__(self, product_spec, test_suite_library, num):
        """
        Initialize this class.

        Arguments:
            test_suite_library - the directory where the test suite will be placed
        """
        assert product_spec is not None, "FileBuilder: Producer spec must not be None"
        assert test_suite_library is not None, "FileBuilder: test suite library must not be null"
        assert len(test_suite_library) > 0, "FileBuilder: test suit library must not be empty"
        assert num is not None, "Test case number must not be None"
        assert num > 0, "Test case number must be greater than 0, not - " + str(num)
        self._product_spec = product_spec
        self._test_suite_library = test_suite_library
        self._num = num
        self._suiteid = product_spec.suite_id
        return

    # ---------------------------------------------------------------------------
    #  Properties
    # ---------------------------------------------------------------------------

    @property
    def test_suite_library(self):
        """Return the name of the directory that will hold the test suite directory"""
        return self._test_suite_library

    @property
    def suite_name(self):
        """Return the name for the test suite"""
        name = self._product_spec.suite_name
        return name

    @property
    def test_suite_dir(self):
        """
        Return the directory path where the test case files will reside.
        """
        direct = self.test_suite_library + "/" + self.suite_name
        return direct

    @property
    def test_case_number(self):
        """
        Return the number of this test case as a string with 4 digits.
        """
        value = str(self._num)
        while len(value) < 4:
            value = "0" + value
        return value

    @property
    def suite_id(self):
        """
        Return the suite id
        """
        return self._suiteid

    @property
    def test_case_filename(self):
        """
        Return the full path name of the test case file.
        """
        name = self.test_suite_dir + "/" + self.test_case_number + "_" + self.suite_id + ".html"
        return name

    @property
    def product_spec(self):
        """Return the product specification"""
        return self._product_spec

    # ---------------------------------------------------------------------------
    #  Operations
    # ---------------------------------------------------------------------------

    def produce_test_case(self):
        """
        Generate a test case file in the test suite directory.
        """
        test_case = TestCase(self.product_spec, self.test_case_number)
        html = test_case.initialize()
        self.output(html)
        return

    def output(self, html):
        """
        Output the HTML to its file.
        """
        file = None
        try:
            file = open(self.test_case_filename, 'w')
            file.write(html)
        except Exception as e:
            raise SuiteDreamsException(e)
        finally:
            if file is not None:
                file.close()
        return
