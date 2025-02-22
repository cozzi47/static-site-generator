import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_with_multiple_props(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_props_to_html_with_no_props(self):
        node = HTMLNode(props=None)
        self.assertEqual(node.props_to_html(), "")
    
    def test_props_to_html_with_complete_node(self):
        node = HTMLNode(tag="p", value="Hello", children=[], props={"class": "greeting"})
        self.assertEqual(node.props_to_html(), ' class="greeting"')

    def test_repr_method_output_for_html_node(self):
        node = HTMLNode(tag="div", value="content")
        self.assertEqual(node.__repr__(), 'HTMLNode(tag=div, value=content, children=None, props=None)')


class TestLeafNode(unittest.TestCase):
    def test_to_html_returns_tag_with_props_and_value(self):
        node = LeafNode(tag="p", value="Hello", props={"class": "greeting"})
        self.assertEqual(node.to_html(), '<p class="greeting">Hello</p>')

    def test_to_html_raises_error_when_value_is_none(self):
        node = LeafNode(tag="p", value=None, props={"class": "greeting"})
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_returns_value_when_tag_is_none(self):
        node = LeafNode(tag=None, value="Hello", props={"class": "greeting"})
        self.assertEqual(node.to_html(), "Hello")

    def test_to_html_returns_tag_with_value_when_no_props(self):
        node = LeafNode(tag="p", value="Hello")
        self.assertEqual(node.to_html(), '<p>Hello</p>')


class TestParentNode(unittest.TestCase):
    def test_to_html_handles_nested_and_nested_leaf_nodes_with_props(self):
        node = ParentNode(
            "div",
            [
                LeafNode("h1", "Hello, world!", props={"class": "title"}),
                ParentNode(
                    "ul",
                    [
                        LeafNode("li", "Item 1", props={"id": "first"}),
                        LeafNode("li", "Item 2"),
                        ParentNode(
                            "li",
                            [LeafNode("span", "Nested item"), LeafNode(None, " (no tag here)")]
                        )
                    ]
                ),
            ],
            props={"class": "container"}
        )
        self.assertEqual(
            node.to_html(), 
            '<div class="container"><h1 class="title">Hello, '
            'world!</h1><ul><li id="first">Item 1</li><li>Item '
            '2</li><li><span>Nested item</span> (no tag here)</li></ul></div>'
        )

    def test_to_html_handles_empty_children(self):
        node = ParentNode("div", [], props={"class": "empty-test"})
        self.assertEqual(node.to_html(), '<div class="empty-test"></div>')

    def test_to_html_with_one_leaf_node_child(self):
        node = ParentNode("section", [LeafNode("p", "Text!")])
        self.assertEqual(node.to_html(), '<section><p>Text!</p></section>')

    def test_to_html_handles_recursive_structure(self):
        node = ParentNode(
            "div",
            [ParentNode("div", [ParentNode("div", [LeafNode("p", "Deep")])])]
        )
        self.assertEqual(node.to_html(), '<div><div><div><p>Deep</p></div></div></div>')

    def test_to_html_handles_empty_and_single_child_mix(self):
        node = ParentNode(
            "section",
            [
                ParentNode("div", []),
                LeafNode("p", "Paragraph"),
            ]
        )
        self.assertEqual(node.to_html(), '<section><div></div><p>Paragraph</p></section>')

    def test_props_to_html_escapes_special_characters(self):
        node = HTMLNode(props={"data-attr": 'quote "test"', "example": "ampersand &"})
        self.assertEqual(
            node.props_to_html(),
            ' data-attr="quote &quot;test&quot;" example="ampersand &amp;"'
        )

    def test_to_html_raises_type_error_for_invalid_children(self):
        with self.assertRaises(TypeError):
            node = ParentNode("div", ["string", 123, LeafNode("p", "Valid")])
            node.to_html()

    def test_to_html_raises_error_when_tag_is_none(self):
        with self.assertRaises(ValueError) as context:
            node = ParentNode(None, [LeafNode("p", "Some text")])
            node.to_html()
        self.assertEqual(str(context.exception), "No tag specified for the HTML node.")
    
    def test_to_html_raises_error_when_children_are_none(self):
        with self.assertRaises(ValueError) as context:
            node = ParentNode("div", None)
            node.to_html()
        self.assertEqual(str(context.exception), "Children attribute cannot be None.")


if __name__ == "__main__":
    unittest.main()