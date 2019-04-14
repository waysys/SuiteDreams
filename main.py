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
from suitedreamsexception import SuiteDreamsException
from filebuilder import FileBuilder
from pathlib import Path
import time
import math
import random


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
    print("Starting SuiteDreams")
    prior = time.time()
    validate(product_spec_filename, test_suite_library)
    validate_test_suite_library(test_suite_library)

    try:
        process(product_spec_filename, test_suite_library)
    except SuiteDreamsException as e:
        print("Error: " + str(e))
        info = sys.exc_info()
        tb = info[2]
        traceback.print_tb(tb)
        sys.exit(1)
    except Exception as e:
        print("Exception: " + str(e))
        info = sys.exc_info()
        tb = info[2]
        traceback.print_tb(tb)
        sys.exit(1)
    finally:
        now = time.time()
        duration = math.ceil(now - prior)
        print("Ending SuiteDreams - " + str(duration) + " seconds")
    sys.exit(0)


def validate(product_spec_filename, test_suite_library):
    """
    Check that the product spec file name and the test suite library directory are not null or empty

    Arguments:
        product_spec_filename - name of product specification file
        test_suite_library - name of directory where the test suite is placed
    """
    if product_spec_filename is None:
        print("Product specification file must not be None")
        sys.exit(1)
    if len(product_spec_filename) == 0:
        print("Product specification file name must not be an empty string")
        sys.exit(1)
    print("Product specification file is " + product_spec_filename)
    if test_suite_library is None:
        print("Test suite library must not be None")
        sys.exit(1)
    if len(test_suite_library) == 0:
        print("Test suite library must not be an empty string")
        sys.exit(1)
    print("Test suite will be generted in directory " + test_suite_library)
    return


def validate_test_suite_library(test_suite_library):
    """
    Check that the test suite library exists and is a directory.

    Arguments:
        test_suite_library - the name of the directory that will hold the test suite directories
    """
    path = Path(test_suite_library)
    if not path.is_dir():
        print("Test suite library does not exist or is not a directory - " + test_suite_library)
        sys.exit(1)
    return


def process(product_spec_filename, test_suite_library):
    """
    Read the product spec and geneerate the number of test cases specified.

    Arguments:
        product_spec_filename - the product specification filename.
        test_suite_library - the path to the directory that will hold the test suite
    """
    #
    # Parse product product_spec
    #
    product_spec = ProductSpec(product_spec_filename)
    product_spec.parse()
    #
    # Validate test suite directory
    #
    suite_name = product_spec.suite_name
    validate_test_suite_dir(test_suite_library, suite_name)
    #
    # Initial random number seed
    #
    seed = product_spec.seed
    random.seed(seed)
    #
    # Get count of test cases to produce
    #
    count = product_spec.count
    print("SuiteDreams is producing " + str(count) + " test cases in test suite " + suite_name)
    #
    # Generate the test cases
    #
    for num in range(count):
        print("Processing testcase " + str(num + 1))
        file_builder = FileBuilder(product_spec, test_suite_library, num + 1)
        file_builder.produce_test_case()
    return


def validate_test_suite_dir(test_suite_library, suite_name):
    """
    Verify that the test suite directory does not exist yeet.
    Then create it.

    Arguments:
         test_suite_library - the diretory that holds test suites.
         suite_name - the name of the test suite.  This will be the name of the subdirectory in
            the test suite library
    """
    if suite_name is None or len(suite_name) == 0:
        raise SuiteDreamsException("Test suite name must not be None or an empty string")
    test_suite_dir = test_suite_library + "/" + suite_name
    path = Path(test_suite_dir)
    if path.exists():
        print("Test suite directory already exists - " + test_suite_dir)
    else:
        path.mkdir(mode=0o777, parents=False, exist_ok=False)
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
