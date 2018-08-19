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
This module tests the product spec class.
"""

import unittest
from productspec import ProductSpec

# -------------------------------------------------------------------------------
#  Test Product Spec
# -------------------------------------------------------------------------------


class TestProductSpec(unittest.TestCase):
    """
    Test the product spec class.
    """

    # ---------------------------------------------------------------------------
    #  Support functions
    # --------------------------------------------------------------------------

    def setUp(self):
        """Create an instance of ProductSpec"""
        self._product_spec = ProductSpec()
        return

    def tearDown(self):
        """Destroy the instance of ProdcutSpec"""
        self._product_spec = None
        return

    # ---------------------------------------------------------------------------
    #  Tests
    # ---------------------------------------------------------------------------

    def test_spec_file_name(self):
        """Test that spec file name can be set and read"""
        filename = "/proj/homeowners.xml"
        self._product_spec.spec_file_name = filename
        self.assertEqual(filename, self._product_spec.spec_file_name)
        return