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
SuiteDreams is a test case generation tool that supports the creation of HTML
test case files used by GFIT.  SuiteDreams reads an XML product specification
and generates multiple test case files by randomly selecting the coverables,
coverages, and values.

This module is the main program for running SuiteDreams.
"""

import sys
from productspec import ProductSpec
import traceback

# -------------------------------------------------------------------------------
#  Main Function
# -------------------------------------------------------------------------------


def main(product_spec_filename, test_suite_library):
    """
    This function is the main controller for SuiteDreams.

    Arguments:
        product_spec_filename - the file name of the product spec
        test_suite_library - the directory that holds test suites
    """
    print("Starting SuiteDreams with product spec " + product_spec_filename)
    print("Test suite will be generted in directory " + test_suite_library)
    try:
        product_spec = ProductSpec()
        product_spec.spec_file_name = product_spec_filename
        process(product_spec)
    except Exception:
        info = sys.exc_info()
        print("Exception: " + str(info[1]))
        tb = info[2]
        traceback.print_tb(tb)
    finally:
        print("Ending SuiteDreams")
    return


def process(product_spec):
    """
    Read the product spec and geneerate the number of test cases specified.

    Arguments:
        product_spec - the instance of the product spec class.
    """
    return

# ---------------------------------------------------------------------------
#  Main
# ---------------------------------------------------------------------------


if __name__ == '__main__':
    """Run the SuiteDreams program"""
    if len(sys.argv) != 3:
        print("""
              To execute SuiteDreams, use this command:
              
              python main.py product_spec_filename test_suite_library
              """)
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])