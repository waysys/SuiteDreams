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
This module tests the TestCase class.
"""

import unittest
from testcase import TestCase
from filebuilder import FileBuilder
from productspec import ProductSpec

filename = "/proj/testsuites/sample.html"
spec_filename = "/proj/SuiteDreams/testsuite1.xml"
test_suite_library = "/proj/SuiteDreams"

# -------------------------------------------------------------------------------
#  Test TestCase
# -------------------------------------------------------------------------------


class TestTestCase(unittest.TestCase):
    """
    This class tests the TestCase class.
    """

    # ---------------------------------------------------------------------------
    #  Support functions
    # --------------------------------------------------------------------------

    def setUp(self):
        """Create an instance of ProductSpec"""
        self._test_case = TestCase(filename)
        self._test_case.initialize()
        self._product_spec = ProductSpec(spec_filename)
        self._product_spec.parse()
        self._file_builder = FileBuilder(self._product_spec, test_suite_library, 1)
        return

    def tearDown(self):
        """Destroy the instance of ProdcutSpec"""
        self._test_case = None
        return

    # ---------------------------------------------------------------------------
    #  Tests
    # ---------------------------------------------------------------------------

    def test_file_structure(self):
        """
        Output the file contents to standard out
        """
        value = ["Comment", "This is a comment"]
        self._test_case.add_row(value)
        self._test_case.dump()
        return

    def test_file_write(self):
        value = ["Comment", "This is a comment"]
        self._test_case.output()
        return

    def test_file_name(self):
        """
        Test the construction of the file name
        """
        name = self._file_builder.test_case_filename
        print(name)
        return


