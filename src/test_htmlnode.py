import unittest
from htmlnode import HTMLNode, LeafNode


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


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode(tag="p", value="Hello", props={"class": "greeting"})
        self.assertEqual(node.to_html(), '<p class="greeting">Hello</p>')

    def test_to_html1(self):
        node = LeafNode(tag="p", value=None, props={"class": "greeting"})
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html2(self):
        node = LeafNode(tag=None, value="Hello", props={"class": "greeting"})
        self.assertEqual(node.to_html(), "Hello")

    def test_to_html3(self):
        node = LeafNode(tag="p", value="Hello")
        self.assertEqual(node.to_html(), '<p>Hello</p>')


if __name__ == "__main__":
    unittest.main()