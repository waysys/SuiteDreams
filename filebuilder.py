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

from suitedreamsexception import SuiteDreamsException
from testcase import TestCase
from productspec import ProductSpec
from pathlib import Path

# -------------------------------------------------------------------------------
#  SuiteBuilder class
# -------------------------------------------------------------------------------


class FileBuilder:
    """
    The File Builder class creates a single test case file in HTML format.
    """

    def __init__(self, producer_spec, test_suite_library):
        """
        Initialize this class.

        Arguments:
            test_suite_library - the directory where the test suite will be placed
        """
        assert producer_spec is not None, "FileBuilder: Producer spec must not be None"
        assert test_suite_library is not None, "FileBuilder: test suite library must not be null"
        assert len(test_suite_library) > 0, "FileBuilder: test suit library must not be empty"
        self._producer_spec = producer_spec
        self._test_suite_library = test_suite_library

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
        name = self._producer_spec.suite_name
        return name

    @property
    def test_suite_dir(self):
        """Return the directory path where the test case files will reside"""
        dir = self.test_suite_library + "/" + self.suite_name
        return dir

    # ---------------------------------------------------------------------------
    #  Operations
    # ---------------------------------------------------------------------------

    def produce_test_case(self):
        """
        Generate a test case file in the test suite directory.
        """
        self.validate_inputs()


        return

    def validate_inputs(self):
        """
        Validate the data:
            -- verify that the test suite library directory exists
            -- create the test suite directory
        """
        path = Path(self.test_suite_library)
        if not path.is_dir():
            raise SuiteDreamsException("Test suite library is not a directory - " + self.test_suite_library)
        path = Path(self.test_suite_dir)
        if path.exists():
            raise SuiteDreamsException("Test suite directory already exists - " + self.test_suite_dir)
        path.mkdir(mode=0o777, parents=False, exist_ok=False)
        return

