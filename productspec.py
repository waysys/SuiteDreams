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
This module contains the class representing the product specification.  
"""

# -------------------------------------------------------------------------------
#  Product Spec class
# -------------------------------------------------------------------------------


class ProductSpec:
    """
    The product spec class represents the information about the insurance product
    that is being tested.
    """

    # ---------------------------------------------------------------------------
    #  Constructor
    # ---------------------------------------------------------------------------

    def __init__(self):
        """
        Initialize this class.
        """
        self._spec_file_name = ""
        return

    # ---------------------------------------------------------------------------
    #  Properties
    # ---------------------------------------------------------------------------

    @property
    def spec_file_name(self):
        """
        Returns: the file name of the XML product specification.
        """
        return self._spec_file_name

    @spec_file_name.setter
    def spec_file_name(self, filename):
        assert filename is not None, "spec_file_name: filename must not be None"
        assert len(filename) > 0, "spec_file_name: filename must not be an emtpy string"
        self._spec_file_name = filename
        return
