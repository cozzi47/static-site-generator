import unittest
from textnode import TextNode, TextType
from markdown_to_textnode import split_nodes_delimiter


class TestMarkdownToTextNode(unittest.TestCase):
    def test_code_text_type(self):
        nodes = [TextNode("Hello `world` there", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "Hello ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "world")
        self.assertEqual(result[1].text_type, TextType.CODE)
        self.assertEqual(result[2].text, " there")
        self.assertEqual(result[2].text_type, TextType.TEXT)

    def test_bold_text_type(self):
        nodes = [TextNode("This is **bold** text", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This is ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "bold")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, " text")
        self.assertEqual(result[2].text_type, TextType.TEXT)

    def test_non_text_node(self):
        nodes = [TextNode("Hello world", TextType.BOLD)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "Hello world")
        self.assertEqual(result[0].text_type, TextType.BOLD)

    def test_no_delimiter(self):
        nodes = [TextNode("Hello world", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "Hello world")
        self.assertEqual(result[0].text_type, TextType.TEXT)

    def test_missing_delimiter(self):
        nodes = [TextNode("Hello `world there", TextType.TEXT)]
        with self.assertRaises(Exception) as context:
            result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(str(context.exception), "No matching delimiter found.")


if __name__ == "__main__":
    unittest.main()