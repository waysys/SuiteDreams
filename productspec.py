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

import xml.etree.ElementTree as Et
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
        self._suite_id = None
        self._project = None
        self._author = None
        self._description = None
        self._seed = None
        self._product_name = None
        self._fixture = None
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

    @property
    def suite_id(self):
        """
        Return the suite id.  This string is used to form the file names for test cases.
        """
        if self._suite_id is None:
            self._suite_id = self.fetch_text(self._root, "SuiteId")
        return self._suite_id

    @property
    def project(self):
        """
        Return the name of the project.
        """
        if self._project is None:
            self._project = self.fetch_text(self._root, "ProjectName")
        return self._project

    @property
    def author(self):
        """
        Return the author of the test case.
        """
        if self._author is None:
            self._author = self.fetch_text(self._root, "Author")
        return self._author

    @property
    def description(self):
        """
        Return the description of the test case.
        """
        if self._description is None:
            self._description = self.fetch_text(self._root, "Description")
        return self._description

    @property
    def fixture(self):
        """Return the fixture to handle this test suite"""
        if self._fixture is None:
            self._fixture = self.fetch_text(self._root, "Fixture")
        return self._fixture

    @property
    def root_element(self):
        """Return the TestSuite element in the product specification"""
        assert self._root is not None, "root_element: root element in product spec must be set"
        return self._root

    @property
    def seed(self):
        """Return the seed for the random number generator"""
        if self._seed is None:
            value = self.fetch_text(self._root, "Seed")
            try:
                self._seed = int(value)
            except ValueError:
                message = "Value for seed is not a valid integer - " + value
                raise SuiteDreamsException(message)
        return self._seed

    @property
    def product_name(self):
        """Return the product name"""
        if self._product_name is None:
            product_element = self.fetch_element(self.root_element, "Product")
            self._product_name = self.fetch_text(product_element, "ProductCode")
        return self._product_name

    @property
    def should_quote(self):
        """
        Return True if the submission should be quoted.
        """
        product_element = self.fetch_element(self.root_element, "Policy")
        has_quote_element = ProductSpec.has_element(product_element, "Quote")
        has_bind_element = ProductSpec.has_element(product_element, "Bind")
        return has_quote_element or has_bind_element

    @property
    def quote_element(self):
        """Return the Quote element"""
        product_element = self.fetch_element(self.root_element, "Policy")
        quote_element = ProductSpec.fetch_element(product_element, "Quote")
        return quote_element

    @property
    def should_bind(self):
        """
        Return True if the submission should be bound.
        """
        product_element = self.fetch_element(self.root_element, "Policy")
        has_bind_element = ProductSpec.has_element(product_element, "Bind")
        return has_bind_element

    # ---------------------------------------------------------------------------
    #  Operations
    # ---------------------------------------------------------------------------

    def parse(self):
        """
        Parse the product spec file
        """
        if not ProductSpec.file_exists(self.spec_file_name):
            raise SuiteDreamsException("Product spec file does not exist - " + self.spec_file_name)
        try:
            tree = Et.parse(self.spec_file_name)
            root = tree.getroot()
            tag = root.tag
            if tag != "TestSuite":
                raise SuiteDreamsException("Root element is not TestSuite - " + tag)
            self._root = root
        except Exception as e:
            raise SuiteDreamsException(str(e))
        return

    @staticmethod
    def file_exists(filename):
        """
        Return true if the file exists and is readable
        """
        file = Path(filename)
        return file.is_file()

    @staticmethod
    def fetch_element(parent, tag):
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
            message = "fetch_element: Element " + tag + " was not found in element " + parent.tag
            raise SuiteDreamsException(message)
        return element

    @staticmethod
    def fetch_text(parent, tag):
        """
        Return the content of an element with the name equal to tag.  If the element is not found,
        an exception is thrown.

        Argument:
            parent - the parent of the element being searched for
            tag - the name of the element to be retrieved

        Returns:
            The content of the element being searched for.
        """
        element = ProductSpec.fetch_element(parent, tag)
        return element.text

    @staticmethod
    def fetch_all_elements(parent, tag):
        """
        Return a list of subelements of the parent with the specified tag.

        Arguments:
            parent - the parent element being searched
            tag - the tag of the element
        """
        assert tag is not None, "fetch_all_element: Tag must not be None"
        assert len(tag) > 0, "fetch_all_element: Tag must not be an empty string"
        assert parent is not None, "fetch_all_element: Parent of element " + tag + " must not be None"
        elements = parent.findall(tag)
        if elements is None:
            elements = []
        return elements

    @staticmethod
    def has_element(parent, tag):
        """
        Return a list of subelements of the parent with the specified tag.

        Arguments:
            parent - the parent element being searched
            tag - the tag of the element
        """
        result = ProductSpec.fetch_all_elements(parent, tag)
        return len(result) > 0
