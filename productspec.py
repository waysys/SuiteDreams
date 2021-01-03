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
__version__ = "02-Jan-2021"

"""
This module contains the class representing the product specification.  
"""

import xml.etree.ElementTree as Et
from pathlib import Path
from suitedreamsexception import SuiteDreamsException
from random import Random
from dates import current_date


# -------------------------------------------------------------------------------
#  XML handler class
# -------------------------------------------------------------------------------

class XmlHandler:
    """
    This class is the parent for the ProductSpec and Fixture classes.
    This class contains generic XML handlers that contain no references
    to the specifics of the schema.
    """

    # ---------------------------------------------------------------------------
    #  Constructor
    # ---------------------------------------------------------------------------

    def __init__(self):
        """
        Initialize this instance of this class.
        """
        return

    # ---------------------------------------------------------------------------
    #  Operations
    # ---------------------------------------------------------------------------

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
        Return true if the parent has  subelements with the specified tag.

        Arguments:
            parent - the parent element being searched
            tag - the tag of the element
        """
        result = ProductSpec.fetch_all_elements(parent, tag)
        return len(result) > 0


# -------------------------------------------------------------------------------
#  Schema Handler class
# -------------------------------------------------------------------------------


class SchemaHandler(XmlHandler):
    """
    This class contains operations that reference features of the
    schema such as weights, but do not reference domain-specific features.
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
        super().__init__()
        self._spec_file_name = filename
        self._root = None
        self._count = None
        self._suite_name = None
        self._suite_id = None
        self._project = None
        self._author = None
        self._description = None
        self._seed = None
        self._fixtures = []
        self._random = Random()
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
    def fixtures(self):
        """Return the fixture to handle this test suite"""
        if len(self._fixtures) == 0:
            fixtures_element = self.fetch_element(self.root_element, "Fixtures")
            elements = self.fetch_all_elements(fixtures_element, "Fixture")
            for element in elements:
                fixture = Fixture(element)
                self._fixtures.append(fixture)
        assert len(self._fixtures) > 0, "Fixture list is empty."
        return self._fixtures

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
    def random_selector(self):
        """Return a random number between 1 and 100"""
        return self._random.randint(1, 100)

    # ---------------------------------------------------------------------------
    #  Parse Operations
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

    # --------------------------------------------------------------------------
    #  Element Operations
    # --------------------------------------------------------------------------

    def fetch_fixture(self, role):
        """
        Retrieve the fixture associated with the specified role from the fixtures list.

        Arguments:
            role - the role associated with the fixture.
        """
        result = None
        for fixture in self.fixtures:
            if fixture.role == role:
                result = fixture.fixture
                break
        return result

    def fetch_property_name_value(self, parent_element, property_name):
        """
        Select the child property elements contained by the parent element.
        Find the property with the specified property name.  Return a
        pair with the property value.
        """
        desired_value = None
        property_elements = self.fetch_all_elements(
            parent_element, "Property")
        for element in property_elements:
            (name, value) = \
                self.process_property(element, "PropertyName", "Value")
            if property_name == name:
                desired_value = value
                break
        return desired_value

    def fetch_property_headings(self, parent_element):
        """
        Return a list of property names to use as headings.  This operation
        is useful for obtaining the column headings for a column fixture.

        Arguments:
            parent_element - the element that contains a set of properties
        """
        headings = []
        property_elements = self.fetch_all_elements(parent_element, "Property")
        for property_element in property_elements:
            (property_name, property_value) = \
                self.process_property(property_element, "PropertyName", "Value")
            headings.append(property_name)
        return headings

    def fetch_property_values(self, parent_element):
        """Return a list of property values to use a values in a column fixture table.

        Arguments:
            parent_element - the element that contains a set of properties
        """
        values = []
        property_elements = self.fetch_all_elements(parent_element, "Property")
        for property_element in property_elements:
            (property_name, property_value) = \
                self.process_property(property_element, "PropertyName", "Value")
            values.append(property_value)
        return values

    def process_property(self, property_element, name_tag, value_tag):
        """
        Return a pair with the property name and selected value.
        If the property is not selected, return the pair (None, None)

        Argument:
            propertyElement - a <Property> element from the product specification
            name_tag - the name of the element that hold the property name
            value_tag - the name of the elements that hold the property values
        """
        result = (None, None)
        property_name = self.fetch_text(property_element, name_tag)
        selector = self.random_selector
        if self.select_element(property_element, selector):
            """Property is selected.  Generate the value for the property."""
            selector = self.random_selector
            value = self.process_values(property_element, property_name, value_tag, selector)
            result = (property_name, value)
        return result

    @staticmethod
    def select_element(element, selector):
        """
        Return true if the selector is less than or equal to the weight on
        the element

        Arguments:
            element - the element being checked
            selector - an integer to compare against the weight
        """
        weight = ProductSpec.fetch_weight(element)
        return selector <= weight

    @staticmethod
    def fetch_weight(element):
        """
        Return the value of the weight attribute as an integer.  This is an integer between 0
        and 100 inclusive.

        Argument:
            element - an XML element that may or may not have a weight attribute
        """
        assert element is not None, "fetch_weight: element must not be None"
        value = element.get("weight", default="100")
        try:
            weight = int(value)
        except ValueError:
            message = "Illegal value for weight attribute in element "
            message += element.tag
            message += " - " + value
            raise SuiteDreamsException(message)
        if weight < 0 or weight > 100:
            message = "Weight on element "
            message += element.tag
            message += " must be between 0 and 100 inclusive, not - " + value
            raise SuiteDreamsException(message)
        return weight

    def process_values(self, property_element, property_name, element_name, selector):
        """
        Select a value from a list of values of a property.

        Argument:
            property_element - the property element containing the values
            property_name - the name of the property or question
            element_name - the name of the element containing values
            selector - a random integer between 0 and 100 inclusive
        """
        assert element_name is not None, "process_values: element name must not be None"
        assert len(element_name) > 0, "process_values: element name must not be an empty string"
        value_elements = self.fetch_all_elements(property_element, element_name)
        sum_weights = 0
        for value_element in value_elements:
            weight = self.fetch_weight(value_element)
            sum_weights += weight
            if selector <= sum_weights:
                return value_element.text
        message = "No values were selected for - " + property_name + ". Element being searched is - " + element_name
        raise SuiteDreamsException(message)

    def fetch_selected_elements(self, parent_element, tag_name):
        """
        Return a list of elements with the specified tag name.  Select only those
        that have been selected based on weight.

        Arguments:
            parent_element - the element containing the degired elements
            tag_name - the name of the elements to be retrieved.
        """
        results = []
        elements = self.fetch_all_elements(parent_element, tag_name)
        for element in elements:
            selector = self.random_selector
            if self.select_element(element, selector):
                results.append(element)
        return results


# -------------------------------------------------------------------------------
#  Product Spec class
# -------------------------------------------------------------------------------


class ProductSpec(SchemaHandler):
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
        super().__init__(filename)
        self._product_name = None
        return

    # ---------------------------------------------------------------------------
    #  Properties
    # ---------------------------------------------------------------------------

    @property
    def product_name(self):
        """Return the product name"""
        if self._product_name is None:
            product_element = self.fetch_element(self.root_element, "Product")
            self._product_name = self.fetch_text(product_element, "ProductCode")
        return self._product_name

    @property
    def account_number(self):
        """
        Return the account number contained by the policy.
        """
        root_element = self.root_element
        policy_element = self.fetch_element(root_element, "Policy")
        acct_num = self.fetch_property_name_value(policy_element, "AccountNumber")
        assert acct_num is not None, "Account number was not found under Policy"
        return acct_num

    @property
    def submission_date(self):
        """
        Return the submission date contained by the policy.  If there is no
        submission date, return the current date.
        """
        root_element = self.root_element
        policy_element = self.fetch_element(root_element, "Policy")
        date = self.fetch_property_name_value(policy_element, "SubmissionDate")
        if date is None:
            date = current_date()
        return date

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

    # --------------------------------------------------------------------------
    #  Domain Operations
    # --------------------------------------------------------------------------

    def fetch_question_sets(self):
        """
        Return a list of question set elements.
        """
        root_element = self.root_element
        product_element = self.fetch_element(root_element, "Product")
        question_set_elements = self.fetch_all_elements(product_element, "QuestionSet")
        return question_set_elements

    def fetch_question_set_code(self, question_set_element):
        """
        Return the question set code for the specified question set element.

        Arguments:
            question_set_element - the element for the question set.
        """
        code = self.fetch_text(question_set_element, "QuestionSetCode")
        return code

    def fetch_questions(self, question_set_element):
        """
        Return a list of questions from the question set.

        Arguments:
            question_set_element - the element for the question set
        """
        elements = self.fetch_all_elements(question_set_element, "Question")
        return elements

    def fetch_question_code_and_answer(self, question_element):
        """
        Return a pair with the code for the question and the answer for the code.

        Arguments:
            question_element - the element containing the answers
        """
        question_code = self.fetch_text(question_element, "QuestionCode")
        answer = self.process_values(question_element, "Question", "Answer", self.random_selector)
        return (question_code, answer)

    def fetch_coverables(self):
        """
        Return a list of coverable elements.
        """
        root = self.root_element
        product_element = self.fetch_element(root, "Product")
        coverable_elements = self.fetch_selected_elements(product_element, "Coverable")
        return coverable_elements

    def fetch_coverages(self, coverable_element):
        """
        Return a list of coverage elements associated with the coverable.

        Arguments:
            coverable_element - the element for a coverable
        """
        coverage_elements = self.fetch_selected_elements(coverable_element, "Coverage")
        return coverage_elements

    def fetch_coverage_code(self, coverage_element):
        """
        Return the code for thie coverage described in the coverage element.

        Arguments:
            coverage_element - the element for the coverage
        """
        coverage_code = self.fetch_text(coverage_element, "CoverageCode")
        return coverage_code

    def fetch_coverage_terms(self, coverage_element):
        """
        Return a list of coverage terms elements associated with
        the coverable.

        Arguments:
            coverage_element - the element for the coverage
            selector - an integer to compare against the weight
        """
        cov_term_elements = self.fetch_all_elements(coverage_element, "CoverageTerm")
        return cov_term_elements

    def fetch_coverage_term_value(self, cov_term_element):
        """
        Return the coverage term value selected at random from the available terms.

        Arguments:
            cov_term_element - the coverage term element
        """
        value = self.process_values(cov_term_element,
                                    "CoverageTerm",
                                    "Term",
                                    self.random_selector)
        return value


# -------------------------------------------------------------------------------
#  Fixture class
# -------------------------------------------------------------------------------


class Fixture(XmlHandler):
    """
    This class models the structure of the fixture element.
    """

    # ---------------------------------------------------------------------------
    #  Constructor
    # ---------------------------------------------------------------------------

    def __init__(self, element):
        """
        Initialize this instance of this class with the text from element.

        Arguments:
            element - the XML Fixture element
        """
        super().__init__()
        self._role = self.fetch_text(element, "Role")
        self._fixture = self.fetch_text(element, "FixtureClass")
        return

    # ---------------------------------------------------------------------------
    #  Properties
    # ---------------------------------------------------------------------------

    @property
    def role(self):
        """
        Return the role this fixture plays.
        """
        return self._role

    @property
    def fixture(self):
        """
        Return the full package name of the fixture.
        """
        return self._fixture
