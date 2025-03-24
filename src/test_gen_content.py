import unittest
from gen_content import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_basic_title(self):
        markdown = "# Simple Title\nSome content"
        self.assertEqual(extract_title(markdown), "Simple Title")
    
    def test_title_with_extra_spaces(self):
        markdown = "#    Title with extra spaces    \nSome content"
        self.assertEqual(extract_title(markdown), "Title with extra spaces")
    
    def test_multiline_markdown(self):
        markdown = "Some text before\n\n# The Real Title\n\nSome text after"
        self.assertEqual(extract_title(markdown), "The Real Title")
    
    def test_no_title(self):
        markdown = "Just some text\nNo title here"
        with self.assertRaises(ValueError):
            extract_title(markdown)
    
    def test_title_with_special_chars(self):
        markdown = "# Title with *special* **chars** and [links](http://example.com)"
        self.assertEqual(extract_title(markdown), "Title with *special* **chars** and [links](http://example.com)")


#class TestGeneratePage(unittest.TestCase):
