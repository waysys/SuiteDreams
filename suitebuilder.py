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
This module holds the SuiteBuilder class.
"""

from suitedreamsexception import SuiteDreamsException

# -------------------------------------------------------------------------------
#  SuiteBuilder class
# -------------------------------------------------------------------------------


class SuiteBuilder:
    """
    The SuiteBuilder class controls the invocation of the FileBuilder instances,
    which generate the test case files.
    """

    def __init__(self, test_suite_library):
        """
        Initialize this class.

        Arguments:
            test_suite_library - the directory where the test suite will be placed
        """
        assert test_suite_library is not None, "SuiteBuilder: test suite library must not be null"
        assert len(test_suite_library) > 0, "SuiteBuilder: test suit library must not be empty"
        self._test_suite_library = test_suite_library

