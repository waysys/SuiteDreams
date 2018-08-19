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
        self._count = None
        self._suite_name = None
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
        Return the number of test cases to be created.
        """
        if self._count is None:
            text = self.fetch_text(self._root, "Count")
            try:
                self._count = int(text)
            except Exception:
                message = "Text in Count element is not a number - '" + text + "'"
                raise SuiteDreamsException(message)
            if self._count < 0:
                message = "Count must not be a negative number - " + text
                raise SuiteDreamsException(message)
        return self._count

    @property
    def suite_name(self):
        """
        Return the name of the test suite.
        """
        if self._suite_name is None:
            self._suite_name = self.fetch_text(self._root, "SuiteName")
        return self._suite_name

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

    def fetch_element(self, parent, tag):
        """
        Return the single element named in the tag argument. This method should be used only when
        only one element with this name is used.  If the element is not found, an exception
        is thrown.

        Argument:
            parent - the parent of the element being searched for
            tag - the name of the element to be retrieved

        Returns:
            The element being searched for.
        """
        assert tag is not None, "fetch_element: Tag must not be None"
        assert len(tag) > 0, "fetch_element: Tag must not be an empty string"
        assert parent is not None, "fetch_element: Parent of element " + tag + " must not be None"
        element = parent.find(tag)
        if element is None:
            message = "Element " + tag + " was not found in element " + parent.tag
            raise SuiteDreamsException(message)
        return element

    def fetch_text(self, parent, tag):
        """
        Return the content of an element with the name equal to tag.  If the element is not found,
        an exception is thrown.

        Argument:
            parent - the parent of the element being searched for
            tag - the name of the element to be retrieved

        Returns:
            The content of the element being searched for.
        """
        element = self.fetch_element(parent, tag)
        return element.text
