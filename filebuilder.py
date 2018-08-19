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
        assert producer_spec is not None, "FileBuilder:"
        assert test_suite_library is not None, "FileBuilder: test suite library must not be null"
        assert len(test_suite_library) > 0, "FileBuilder: test suit library must not be empty"
        self._producer_spec = producer_spec
        self._test_suite_library = test_suite_library

    # ---------------------------------------------------------------------------
    #  Operations
    # ---------------------------------------------------------------------------

    def produce_test_case(self):
        """
        Generate a test case file in the test suite directory.
        """
        return
