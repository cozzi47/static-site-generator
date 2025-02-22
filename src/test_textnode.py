import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq2(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, None)
        self.assertEqual(node, node2)
    
    def test_not_eq_false(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_not_eq_false2(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_false3(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        self.assertNotEqual(node, node2)


class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_text_node_to_html_node_text(self):
        node = TextNode("This is text", TextType.TEXT)
        html_node = node.text_node_to_html_node()
        self.assertIsNone(html_node.tag)
        self.assertEqual(html_node.value, "This is text")
        self.assertIsNone(html_node.props)

    def test_text_node_to_html_node_bold(self):
        node = TextNode("This is text", TextType.BOLD)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is text")
        self.assertIsNone(html_node.props)

    def test_text_node_to_html_node_italic(self):
        node = TextNode("This is text", TextType.ITALIC)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is text")
        self.assertIsNone(html_node.props)

    def test_text_node_to_html_node_code(self):
        node = TextNode("This is text", TextType.CODE)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is text")
        self.assertIsNone(html_node.props)
    
    def test_text_node_to_html_node_link(self):
        node = TextNode("This is text", TextType.LINK, "https://www.boot.dev")
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is text")
        self.assertEqual(html_node.props, {"href": "https://www.boot.dev"})

    def test_text_node_to_html_node_image(self):
        node = TextNode("This is text", TextType.IMAGE, "https://www.boot.dev")
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://www.boot.dev", "alt": "This is text"})

    def test_text_node_to_html_node_error(self):
        node = TextNode("This is text", "invalid_type")
        with self.assertRaises(Exception) as context:
            node.text_node_to_html_node()
        self.assertEqual(str(context.exception), "Invalid text type")


if __name__ == "__main__":
    unittest.main()