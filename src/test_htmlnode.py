import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_props_to_html1(self):
        node = HTMLNode(props=None)
        self.assertEqual(node.props_to_html(), "")
    
    def test_complete_node(self):
        node = HTMLNode(tag="p", value="Hello", children=[], props={"class": "greeting"})
        self.assertEqual(node.props_to_html(), ' class="greeting"')

    def test_repr(self):
        node = HTMLNode(tag="div", value="content")
        self.assertEqual(node.__repr__(), 'HTMLNode(tag=div, value=content, children=None, props=None)')


if __name__ == "__main__":
    unittest.main()