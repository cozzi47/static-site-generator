import unittest
import re
from textnode import TextNode, TextType
from markdown_to_textnode import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link
    )



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


class TestExtractMarkdown(unittest.TestCase):
    def test_plain_text(self):
        text = "This is just plain text without any markdown syntax."
        extracted_images = extract_markdown_images(text)
        extracted_links = extract_markdown_links(text)
        self.assertEqual(extracted_images, [])
        self.assertEqual(extracted_links, [])

    def test_single_image(self):
        text = "Here is an image: ![alt text](https://image.url)."
        extracted_images = extract_markdown_images(text)
        extracted_links = extract_markdown_links(text)
        self.assertEqual(extracted_images, [("alt text", "https://image.url")])
        self.assertEqual(extracted_links, [])

    def test_single_link(self):
        text = "Here is a link: [example](https://example.com)."
        extracted_images = extract_markdown_images(text)
        extracted_links = extract_markdown_links(text)
        self.assertEqual(extracted_images, [])
        self.assertEqual(extracted_links, [("example", "https://example.com")])

    def test_multiple_images_and_links(self):
        text = "![image1](url1) ![image2](url2) [link1](url1) [link2](url2)"
        extracted_images = extract_markdown_images(text)
        extracted_links = extract_markdown_links(text)
        self.assertEqual(extracted_images, [("image1", "url1"), ("image2", "url2")])
        self.assertEqual(extracted_links, [("link1", "url1"), ("link2", "url2")])

    def test_malformed_markdown(self):
        text = "![broken image](missingurl"
        extracted_images = extract_markdown_images(text)
        extracted_links = extract_markdown_links(text)
        self.assertEqual(extracted_images, [])
        self.assertEqual(extracted_links, [])


class TestSplitNodes(unittest.TestCase):
    def test_empty_list(self):
        self.assertEqual(split_nodes_link([]), [])
        self.assertEqual(split_nodes_image([]), [])

    def test_no_links_or_images(self):
        node = TextNode("plain text", TextType.TEXT)
        self.assertEqual(split_nodes_link(node), [node])
        self.assertEqual(split_nodes_image(node), [node])

    def test_single_link(self):
        node = TextNode("this is a link [anchor text](link)", TextType.TEXT)
        self.assertEqual(
            split_nodes_link(node), [
            TextNode("this is a link ", TextType.TEXT),
            TextNode("anchor text", TextType.LINK, "link")
            ]
        )

    def test_multiple_images(self):
        node = TextNode("![alt1](img1) and another ![alt2](img2)", TextType.TEXT)
        self.assertEqual(
            split_nodes_image(node), [
            TextNode("alt1", TextType.IMAGE, "img1"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("alt2", TextType.IMAGE, "img2")
            ]
        )

    def test_multiple_links_no_text(self):
        node = TextNode("multiple links [anchor1](link1)[anchor2](link2) more text", TextType.TEXT)
        self.assertEqual(
            split_nodes_link(node), [
            TextNode("multiple links ", TextType.TEXT),
            TextNode("anchor1", TextType.LINK, "link1"),
            TextNode("anchor2", TextType.LINK, "link2"),
            TextNode(" more text", TextType.TEXT)
            ]
        )

    def test_special_characters(self):
        node = TextNode("[text](https://example.com/path?param=value#section)", TextType.TEXT)
        self.assertEqual(
            split_nodes_link(node), [
            TextNode(
                "text", TextType.LINK,
                "https://example.com/path?param=value#section"
                )
            ]
        )

    def test_edge_positions(self):
        node = TextNode("[start](link1) middle [end](link2)", TextType.TEXT)
        # what should the result look like?

    def test_non_text_node(self):
        node = TextNode("text", TextType.BOLD)
        # what should happen here?


if __name__ == "__main__":
    unittest.main()