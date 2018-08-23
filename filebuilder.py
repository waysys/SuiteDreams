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
__version__ = "1.00"

"""
This module holds the FileBuilder class. 
"""

# from suitedreamsexception import SuiteDreamsException
from testcase import TestCase

# -------------------------------------------------------------------------------
#  SuiteBuilder class
# -------------------------------------------------------------------------------


class FileBuilder:
    """
    The File Builder class creates a single test case file in HTML format.
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
        self._test_case = None
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
        suiteid = self._product_spec.suite_id
        return suiteid

    @property
    def test_case_filename(self):
        """
        Return the full path name of the test case file.
        """
        name = self.test_suite_dir + "/" + self.test_case_number + "_" + self.suite_id + ".html"
        return name

    @property
    def test_case(self):
        """
        Return the test case object.
        """
        assert self._test_case is not None, "test_case: test case must not be null"
        return self._test_case

    @test_case.setter
    def test_case(self, value):
        """
        Set the value of the test case.

        Argument:
            value - the new value of the test case
        """
        assert value is not None, "test_case: test case value must not be None"
        self._test_case = value
        return

    @property
    def test_id(self):
        """
        Return the test id for this test
        """
        testid = "TEST-" + self.suite_id + "-" + self.test_case_number
        return testid

    @property
    def public_id(self):
        """
        Return the value of the public id
        """
        publicid = self.suite_id + "-" + self.test_case_number
        return publicid

    # ---------------------------------------------------------------------------
    #  Operations
    # ---------------------------------------------------------------------------

    def produce_test_case(self):
        """
        Generate a test case file in the test suite directory.
        """
        self._test_case = TestCase(self.test_case_filename)
        self.initialize()
        self.test_case.initialize()
        self.process_policy()
        self.test_case.output()
        return

    def initialize(self):
        """
        Set the properties on the test case.
        """
        self.test_case.title = self._product_spec.suite_name
        self.test_case.project = self._product_spec.project
        self.test_case.author = self._product_spec.author
        self.test_case.description = self._product_spec.description
        return

    def process_policy(self):
        """
        Place the initial rows into the table
        """
        self.add_set_value("Test Id", self.test_id)
        attrib = {"class" : "unique"}
        self.add_set_value("PublicID", self.public_id, attrib)

    def add_set_value(self, prop, value, attrib=None):
        """
        Add a row to the table to set a value on the fixture.

        Arguments:
            prop - the fixture property to receive a value
            value - the value for the property
        """
        row = ["set", prop, "to", value, ""]
        if attrib is None:
            self.test_case.add_row(row)
        else:
            self.test_case.add_row_attrib(row, attrib)
        return
