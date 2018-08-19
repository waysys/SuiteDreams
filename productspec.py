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

import xml.etree.ElementTree as ET
from pathlib import Path
from suitedreamsexception import SuiteDreamsException

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

    def __init__(self, filename):
        """
        Initialize this class.

        Arguments:
            filename - the full path to the product spec file
        """
        self._spec_file_name = filename
        self._root = None
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

    @property
    def count(self):
        """
        Return the numbber of test cases to be created.
        """

        return

    # ---------------------------------------------------------------------------
    #  Operations
    # ---------------------------------------------------------------------------

    def parse(self):
        """
        Parse the product spec file
        """
        if not self.file_exists(self.spec_file_name):
            raise SuiteDreamsException("Product spec file does not exist - " + self.spec_file_name)
        try:
            tree = ET.parse(self.spec_file_name)
            root = tree.getroot()
            tag = root.tag
            if tag != "TestSuite":
                raise SuiteDreamsException("Root element is not TestSuite - " + tag)
            self._root = root
        except Exception as e:
            raise SuiteDreamsException(str(e))
        return

    def file_exists(self, filename):
        """
        Return true if the file exists and is readable
        """
        file = Path(filename)
        return file.is_file()
