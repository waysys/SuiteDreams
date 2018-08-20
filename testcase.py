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
The test case module contains the TestCase class.
"""

from xml.etree.ElementTree import Element
from xml.etree.ElementTree import tostring
from suitedreamsexception import SuiteDreamsException
from xml.dom import minidom
from _datetime import date


# -------------------------------------------------------------------------------
#  Test Case Class
# -------------------------------------------------------------------------------


class TestCase:
    """
    The TestCase class models an HTML file used for GFIT test cases.
    """

    # ---------------------------------------------------------------------------
    #  Constructor
    # ---------------------------------------------------------------------------

    def __init__(self, filename):
        """
        Initialize the class.

        Argument:
            filename - the name of the file to be created.
        """
        assert filename is not None, "TestCase: File name must not be None"
        assert len(filename) > 0, "TestCase: File name must not be an empty string"
        self._filename = filename
        self._html = None
        self._title = "Test Case"
        self._project = "My Project"
        self._author = "Tester"
        self._description = "Test case description"
        self._table = None
        return

    # ---------------------------------------------------------------------------
    #  Properties
    # ---------------------------------------------------------------------------

    @property
    def title(self):
        """
        This property holds the content that goes into the <title> element in
        the heading.
        """
        return self._title

    @title.setter
    def title(self, content):
        """
        Set the value of the title.

        Argument:
            content - the title of the test page
        """
        if content is None:
            message = "Title of test case must not be None"
            raise SuiteDreamsException(message)
        if len(content) == 0:
            message = "Title of test case must not be empty"
            raise SuiteDreamsException(message)
        self._title = content
        return

    @property
    def project(self):
        """
        Return the name of the project.
        """
        return self._project

    @project.setter
    def project(self, name):
        """
        Set the name of the project.

        Argument:
            name - the name of the project
        """
        assert name is not None, "project: Project name must not be null"
        assert len(name) > 0, "project: Project name must not be an empty string."
        self._project = name
        return

    @property
    def author(self):
        """
        Return the author of this test case.
        """
        return self._author

    @author.setter
    def author(self, name):
        """
        Set the name of the author.

        Argument:
            name - the name of the author
        """
        assert name is not None, "author: Author must not be None"
        assert len(name) > 0, "author: Author must not be an empty string"
        self._author = name
        return

    @property
    def description(self):
        """
        Return a description of the test case.
        """
        return self._description

    @description.setter
    def description(self, desc):
        """
        Set the description for the project.
        """
        assert desc is not None, "description: description must not be null"
        self._description = desc
        return

    @property
    def table(self):
        """
        Return the table element where the rows go.
        """
        return self._table

    # ---------------------------------------------------------------------------
    #  Element Creation Operations
    # ---------------------------------------------------------------------------

    def initialize(self):
        """
        Create the initial hierarchy of a test case file.
        """
        root = TestCase.create_html()
        head = self.create_head()
        root.append(head)
        body = self.create_body()
        root.append(body)
        self._html = root
        return

    @staticmethod
    def create_html():
        """
        Return an HTML element with the namespace defined

        Returns:
            HTML element
        """
        attrib = {
            "xmlns": "http://www.w3.org/1999/xhtml",
            "xml:lang": "en"
        }
        root = Element("html", attrib)
        return root

    def create_head(self):
        """
        Return the head element.
        """
        head = Element("head")
        tle = Element("title")
        tle.text = self.title
        head.append(tle)
        style = TestCase.create_style()
        head.append(style)
        return head

    @staticmethod
    def create_style():
        """
        Create the style element that defines the unique and claimnumber classes.
        """
        attrib = {
            "type": "text/css"
        }

        style = Element("style", attrib)
        css = """
              td.unique
              {
                color : red;
                font : bold
              }
              td.claimnumber
              {
                color : purple;
                font  : bold
              }
              """
        style.text = css
        return style

    def create_body(self):
        """
        Create the body element
        """
        body = Element("body")
        test_description = self.create_test_description()
        body.append(test_description)
        hr = Element("hr")
        body.append(hr)
        h2 = Element("h2")
        h2.text = self.title
        body.append(h2)
        table = self.create_table()
        body.append(table)
        return body

    def create_test_description(self):
        """
        Create a descripton list element with information about the test case.
        """
        dl = Element("dl")
        TestCase.create_dl_dt(dl, "Project:", self.project)
        TestCase.create_dl_dt(dl, "Author:", self.author)
        adate = str(date.today())
        TestCase.create_dl_dt(dl, "Date:", adate)
        TestCase.create_dl_dt(dl, "Repeatable:", "Yes")
        TestCase.create_dl_dt(dl, "Description:", self.description)
        return dl

    @staticmethod
    def create_dl_dt(dl, term, description):
        """
        Create a par of element (dt and dd) and append them to a dl element

        Arguments:
            dl - a dl element
            term - the content of the dt element
            description - the content of the dd element
        """
        dt = Element("dt")
        dt.text = term
        dd = Element("dd")
        dd.text = description
        dl.append(dt)
        dl.append(dd)
        return

    def create_table(self):
        """Create a table element"""
        attrib = {"border": "1"}
        table = Element("table", attrib)
        self._table = table
        return table

    def add_row(self, values):
        """
        Add a row to the table in the test case.

        Argument:
            values - a list of between 1 and 5 strings for the content of the row
        """
        assert values is not None
        assert len(values) > 0, "add_row: there must be at least one value in a row"
        assert len(values) < 6, "add_row: there must be no more than 5 values in a row"
        tr = Element("tr")
        for value in values:
            td = Element("td")
            td.text = value
            tr.append(td)
        self.table.append(tr)
        return

    # ---------------------------------------------------------------------------
    #  Output Operations
    # ---------------------------------------------------------------------------

    @staticmethod
    def prettify(elem):
        """
        Return a pretty-printed XML string for the element elem.
        """
        rough_string = tostring(elem, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")

    def dump(self):
        """
        Output the file to standard out.
        """
        print(TestCase.prettify(self._html))
        return

    def output(self):
        """
        Output the HTML to its file.
        """
        file = None
        try:
            file = open(self._filename, 'w')
            result = TestCase.prettify(self._html)
            file.write(result)
        except Exception as e:
            raise SuiteDreamsException(e)
        finally:
            if file is not None:
                file.close()
        return
