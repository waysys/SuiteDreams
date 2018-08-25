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
from testcase import TestCase
import random


# -------------------------------------------------------------------------------
#  SuiteBuilder class
# -------------------------------------------------------------------------------


class FileBuilder:
    """
    The File Builder class creates a single test case file in HTML format.
    """

    def __init__(self, product_spec, test_suite_library, num):
        """
        Initialize this class.

        Arguments:
            test_suite_library - the directory where the test suite will be placed
        """
        assert product_spec is not None, "FileBuilder: Producer spec must not be None"
        assert test_suite_library is not None, "FileBuilder: test suite library must not be null"
        assert len(test_suite_library) > 0, "FileBuilder: test suit library must not be empty"
        assert num is not None, "Test case number must not be None"
        assert num > 0, "Test case number must be greater than 0, not - " + str(num)
        self._product_spec = product_spec
        self._test_suite_library = test_suite_library
        self._num = num
        self._test_case = None
        #
        # Set the seed for the random number generator
        #
        seed = product_spec.seed
        random.seed(seed)
        return

    # ---------------------------------------------------------------------------
    #  Properties
    # ---------------------------------------------------------------------------

    @property
    def test_suite_library(self):
        """Return the name of the directory that will hold the test suite directory"""
        return self._test_suite_library

    @property
    def suite_name(self):
        """Return the name for the test suite"""
        name = self._product_spec.suite_name
        return name

    @property
    def test_suite_dir(self):
        """
        Return the directory path where the test case files will reside.
        """
        direct = self.test_suite_library + "/" + self.suite_name
        return direct

    @property
    def test_case_number(self):
        """
        Return the number of this test case as a string with 4 digits.
        """
        value = str(self._num)
        while len(value) < 4:
            value = "0" + value
        return value

    @property
    def suite_id(self):
        """
        Return the suite id
        """
        suiteid = self._product_spec.suite_id
        return suiteid

    @property
    def test_case_filename(self):
        """
        Return the full path name of the test case file.
        """
        name = self.test_suite_dir + "/" + self.test_case_number + "_" + self.suite_id + ".html"
        return name

    @property
    def test_case(self):
        """
        Return the test case object.
        """
        assert self._test_case is not None, "test_case: test case must not be null"
        return self._test_case

    @test_case.setter
    def test_case(self, value):
        """
        Set the value of the test case.

        Argument:
            value - the new value of the test case
        """
        assert value is not None, "test_case: test case value must not be None"
        self._test_case = value
        return

    @property
    def test_id(self):
        """
        Return the test id for this test
        """
        testid = "TEST-" + self.suite_id + "-" + self.test_case_number
        return testid

    @property
    def public_id(self):
        """
        Return the value of the public id
        """
        publicid = self.suite_id + "-" + self.test_case_number
        return publicid

    @property
    def product_spec(self):
        """Return the product specification"""
        return self._product_spec

    @property
    def product_spec_root(self):
        """Return the root of the product specification"""
        return self.product_spec.root_element

    @property
    def random_selector(self):
        """Return a random number between 1 and 100"""
        return random.randint(1, 100)

    # ---------------------------------------------------------------------------
    #  Operations
    # ---------------------------------------------------------------------------

    def produce_test_case(self):
        """
        Generate a test case file in the test suite directory.
        """
        self._test_case = TestCase(self.test_case_filename)
        self.initialize()
        self.test_case.initialize()
        self.process_policy()
        self.process_product()
        self.process_quote()
        self.process_bind()
        self.test_case.output()
        return

    def initialize(self):
        """
        Set the properties on the test case.
        """
        self.test_case.title = self.product_spec.suite_name
        self.test_case.project = self.product_spec.project
        self.test_case.author = self.product_spec.author
        self.test_case.description = self.product_spec.description
        return

    # ---------------------------------------------------------------------------
    #  Operations for Policy
    # ---------------------------------------------------------------------------

    def process_policy(self):
        """
        Place the initial rows into the table
        """
        #
        # Create the fixture row.
        #
        self.add_command(self.product_spec.fixture)
        #
        # Create predefined rows
        #
        self.add_set_value("Test Id", self.test_id)
        attrib = {"class": "unique"}
        self.add_set_value("PublicID", self.public_id, attrib)
        self.add_set_value("Quote Type", "Full")
        product_name = self.product_spec.product_name
        self.add_set_value("Product Code", product_name)
        #
        # Add variable rows based on Policy element in product specification.
        #
        root_element = self.product_spec_root
        policy_element = self.product_spec.fetch_element(root_element, "Policy")
        property_elements = self.product_spec.fetch_all_elements(policy_element, "Property")
        for property_element in property_elements:
            self.process_property(property_element)
        #
        # Add final commands
        #
        self.add_create_policy()
        self.add_check_property("Status", "New")
        self.add_command("edit")
        self.add_check_property("Status", "Draft")
        return

    def process_property(self, property_element):
        """
        Add a set property element to the test cases if it is selected

        Argument:
            propertyElement - a <Property> element from the product specification
        """
        property_name = self.product_spec.fetch_text(property_element, "PropertyName")
        selector = self.random_selector
        if FileBuilder.select_element(property_element, selector):
            """Property is selected.  Generate the value for the property."""
            value = self.process_values(property_element, property_name, "Value")
            self.add_set_value(property_name, value)
        return

    # ---------------------------------------------------------------------------
    #  Operations for Product
    # ---------------------------------------------------------------------------

    def process_product(self):
        """Process the <Product> element """
        product_element = self.product_spec.fetch_element(self.product_spec_root, "Product")
        self.process_question_sets(product_element)
        self.process_coverables(product_element)

    def process_question_sets(self, product_element):
        """
        Process any questions sets

        Arguments:
            product_element - the <Product> element
        """
        question_set_elements = self.product_spec.fetch_all_elements(product_element, "QuestionSet")
        for question_set_element in question_set_elements:
            """Process eache question set"""
            self.process_question_set(question_set_element)
        return

    def process_question_set(self, question_set_element):
        """
        Output the questions from a questions set.  A question set is a grouping of questions.

        Argument:
            question_set_element - a <QuestionSet> element
        """
        question_set_code = self.product_spec.fetch_text(question_set_element, "QuestionSetCode")
        question_elements = self.product_spec.fetch_all_elements(question_set_element, "Question")
        if len(question_elements) == 0:
            message = "Question set does not have any questions - " + question_set_code
            raise SuiteDreamsException(message)
        for question_element in question_elements:
            self.process_question(question_element, question_set_code)
        return

    def process_question(self, question_element, question_set_code):
        """
        Process a questions with its answers.

        Arguments:
            question_element - the <Question> element
            question_set_code - the code identifying the questions set
        """
        question_code = self.product_spec.fetch_text(question_element, "QuestionCode")
        value = self.process_values(question_element, question_code, "Answer")
        self.add_question(question_set_code, question_code, value)

    # ---------------------------------------------------------------------------
    #  Operations for Coverables
    # ---------------------------------------------------------------------------

    def process_coverables(self, product_element):
        """
        Process the sset of coverables.

        Arguments:
            product_element - the <Product> element
        """
        coverable_elements = self.product_spec.fetch_all_elements(product_element, "Coverable")
        if len(coverable_elements) == 0:
            message = "Product must have at least one coverable"
            raise SuiteDreamsException(message)
        for coverable_element in coverable_elements:
            selector = self.random_selector
            if FileBuilder.select_element(coverable_element, selector):
                self.process_coverable(coverable_element)
        return

    def process_coverable(self, coverable_element):
        """
        Output the rows for a coverable including setting property values and coverages

        Argument:
            coverable_element - a <Coverable> element
        """
        coverable_name = self.product_spec.fetch_text(coverable_element, "CoverableName")
        property_elements = self.product_spec.fetch_all_elements(coverable_element, "Property")
        #
        # Output the "select coverable" or "create coverable" row only if there are properties
        # to set.
        #
        if len(property_elements) > 0:
            if FileBuilder.is_coverable_created(coverable_element):
                self.add_create_coverable(coverable_name)
            else:
                self.add_select_coverable(coverable_name)
            #
            #  Output set_select rows to set property values
            #
            for property_element in property_elements:
                self.process_coverable_property(property_element)
            #
            # Output "commit coverable" row.
            #
            self.add_commit("coverable")
        #
        # Output coverages
        #
        coverage_elements = self.product_spec.fetch_all_elements(coverable_element, "Coverage")
        for coverage_element in coverage_elements:
            self.process_coverage(coverage_element, coverable_name)
        return

    def process_coverable_property(self, property_element):
        """
        Add a set property element to the test cases if it is selected

        Argument:
            propertyElement - a <Property> element from the product specification
        """
        property_name = self.product_spec.fetch_text(property_element, "PropertyName")
        selector = self.random_selector
        if FileBuilder.select_element(property_element, selector):
            """Property is selected.  Generate the value for the property."""
            value = self.process_values(property_element, property_name, "Value")
            self.add_set_select_value(property_name, value)
        return

    # ---------------------------------------------------------------------------
    #  Operations for Coverages
    # ---------------------------------------------------------------------------

    def process_coverage(self, coverage_element, coverable_name):
        """
        Output the rows for creating a coverage on a coverable

        Arguments:
            coverage_element - a <Coverage> element
            coverable_name - the name of the coverable
        """
        #
        # Determine if this coverage is going to be output.
        #
        selector = self.random_selector
        if self.select_element(coverage_element, selector):
            coverage_code = self.product_spec.fetch_text(coverage_element, "CoverageCode")
            self.add_create_coverage(coverage_code, coverable_name)
            coverage_term_elements = self.product_spec.fetch_all_elements(coverage_element, "CoverageTerm")
            for coverage_term_element in coverage_term_elements:
                self.process_coverage_term(coverage_term_element)
            self.add_commit("coverage")
        return

    def process_coverage_term(self, coverage_term_element):
        """
        Process the coverage term element.

        Argument:
            coverage_term_element - a <CoverageTerm> element
        """
        coverage_term_code = self.product_spec.fetch_text(coverage_term_element, "CoverageTermCode")
        term_elements = self.product_spec.fetch_all_elements(coverage_term_element, "Term")
        if len(term_elements) == 0:
            message = "Coverage term must have terms - " + coverage_term_code
            raise SuiteDreamsException(message)
        value = self.process_values(coverage_term_element, coverage_term_code, "Term")
        self.add_with(coverage_term_code, value)
        return

    # ---------------------------------------------------------------------------
    #  Operations for Quote and Bind
    # ---------------------------------------------------------------------------

    def process_quote(self):
        """
        Output the rows to have the submission quoted
        """
        if self.product_spec.should_quote:
            self.add_check_property("CanRequestQuote", "true")
            self.add_command("quote")
            self.add_check_property("Status", "Quoted")
        return

    def process_bind(self):
        """
        Output the rows to have the submission bound.
        """
        if self.product_spec.should_bind:
            self.add_check_property("CanBind", "true")
            self.add_command("bind")
            self.add_check_property("Status", "Bound")
        return

    # ---------------------------------------------------------------------------
    #  Operations on Xml elements
    # ---------------------------------------------------------------------------

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

    @staticmethod
    def select_element(element, selector):
        """
        Return true if the selector is less than or equal to the weight on
        the element

        Arguments:
            element - the element being checked
            selector - an integer to compare against the weight
        """
        weight = FileBuilder.fetch_weight(element)
        return selector <= weight

    def process_values(self, property_element, property_name, element_name):
        """
        Select a value from a list of values of a property.

        Argument:
            property_element - the property element containig the values
            property_name - the name of the property or question
            element_name - the name of the element containing values
        """
        assert element_name is not None, "process_values: element name must not be None"
        assert len(element_name) > 0, "process_values: element name must not be an empty string"
        selector = self.random_selector
        value_elements = self.product_spec.fetch_all_elements(property_element, element_name)
        sum_weights = 0
        for value_element in value_elements:
            weight = FileBuilder.fetch_weight(value_element)
            sum_weights += weight
            if selector <= sum_weights:
                return value_element.text
        message = "No values were selected for - " + property_name + ". Element being searched is - " + element_name
        raise SuiteDreamsException(message)

    @staticmethod
    def is_coverable_created(coverage_element):
        """Return true if the coverage is to be created"""
        select = coverage_element.get("select")
        if select is None:
            result = False
        elif select == "create":
            result = True
        elif select == "select":
            result = False
        else:
            message = "Invalid value for select attribute on <Coverable> element - " + select
            raise SuiteDreamsException(message)
        return result

    # ---------------------------------------------------------------------------
    #  Operations to add rows to the test case
    # ---------------------------------------------------------------------------

    def add_set_value(self, prop, value, attrib=None):
        """
        Add a row to the table to set a value on the fixture.

        Arguments:
            prop - the fixture property to receive a value
            value - the value for the property
        """
        row = ["set", prop, "to", value, ""]
        if attrib is None:
            self.test_case.add_row(row)
        else:
            self.test_case.add_row_attrib(row, attrib)
        return

    def add_create_policy(self):
        """
        Add a row to create a policy.
        """
        row = ["create", "policy"]
        self.test_case.add_row(row)
        return

    def add_check_property(self, prop, value):
        """
        Add a row to check the value of a property.

        Arguments:
            prop - a property
            value - the value the property should have
        """
        row = ["check", prop, "as", value]
        self.test_case.add_row(row)
        return

    def add_command(self, command):
        """Add a row to perform a command

        Argument:
            command - the command to be performed
        """
        row = [command]
        self.test_case.add_row(row)
        return

    def add_question(self, question_set_code, question_code, answer):
        """Add a row to the test case with a question and answer.
        Arguments:
            question_set_code - the code for the question set
            question_code - the code for the question
            answer - the answer to the question
        """
        row = ["answer", question_set_code, question_code, answer]
        self.test_case.add_row(row)
        return

    def add_set_select_value(self, prop, value):
        """Add a row to the table for setting a property on a coverable.

        Arguments:
            prop - the fixture property to receive a value
            value - the value for the property
        """
        row = ["set_select", prop, "as", value]
        self.test_case.add_row(row)
        return

    def add_create_coverable(self, coverable_name):
        """
        Add a row to the table for creating a coverable.

        Argument:
            coverable_name - name of the coverable
        """
        row = ["create", coverable_name]
        self.test_case.add_row(row)
        return

    def add_select_coverable(self, coverable_name):
        """
        Add a row to the table for selecting a coverable.

        Argument:
            coverable_name - name of the coverable
        """
        row = ["select", coverable_name]
        self.test_case.add_row(row)
        return

    def add_commit(self, entity):
        """
        Add a row to the table for committing the coverable.

        Arguments:
            entity - either coverable or coverage
        """
        assert entity in ["coverable", "coverage"]
        row = ["commit", entity]
        self.test_case.add_row(row)
        return

    def add_create_coverage(self, coverage_code, coverable_name):
        """
        Add a row to the table for creating a coverage

        Arguments:
            coverage_code - the code from the product model for the coverage
            coverable_name - the name of the coverable
        """
        row = ["create", "coverage", coverage_code, "on", coverable_name]
        self.test_case.add_row(row)
        return

    def add_with(self, coverage_term_code, value):
        """
        Add the with row to the table

        Arguments:
            coverage_term_code - the code for the coverage term
            value - the value for the term
        """
        row = ["with", coverage_term_code, "to", value]
        self.test_case.add_row(row)
        return
