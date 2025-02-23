import unittest
import re
from extract_markdown import extract_markdown_images, extract_markdown_links


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


if __name__ == "__main__":
    unittest.main()