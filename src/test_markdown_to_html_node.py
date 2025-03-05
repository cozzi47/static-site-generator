import unittest
from markdown_to_html_node import markdown_to_html_node


class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_paragraph(self):
        md = "This is a paragraph."
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is a paragraph.</p></div>"
        )

    def test_bold_and_italic(self):
        md = "This is **bold** and _italic_ text."
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bold</b> and <i>italic</i> text.</p></div>"
        )

    def test_code_block(self):
        md = "```\ndef hello():\n    print('world')\n```"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>def hello():\n    print('world')</code></pre></div>"
        )

    def test_ordered_list(self):
        md = "1. First item\n2. Second item\n3. Third item"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second item</li><li>Third item</li></ol></div>"
        )

    def test_unordered_list(self):
        md = "- First item\n- Second item\n- Third item"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>First item</li><li>Second item</li><li>Third item</li></ul></div>"
        )

    def test_empty_code_block(self):
        md = "``` ```"
        node = markdown_to_html_node(md)
        html = node.to_html() if node else ""
        self.assertEqual(
            html,
            "<div><pre><code> </code></pre></div>"
        )
