import unittest
from markdown_to_blocks import (
    markdown_to_blocks,
    block_to_block_type,
    BlockType
)


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
            This is **bolded** paragraph

            This is another paragraph with _italic_ text and `code` here
            This is the same paragraph on a new line

            - This is a list
            - with items
            """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


class TestBlockToBlockType(unittest.TestCase):
    def test_paragraph(self):
        block = "This is a simple paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        
        block = "This is a paragraph\nwith multiple lines."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_heading(self):
        block = "# Heading 1"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        
        block = "## Heading 2"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        
        block = "###### Heading 6"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        
        # Invalid heading (no space after #)
        block = "#Invalid heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_code(self):
        block = "```\ncode block\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        
        block = "```\nMultiple lines\nof code\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        
        # Missing end backticks
        block = "```\nIncomplete code block"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_quote(self):
        block = ">This is a quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        
        block = ">Line 1\n>Line 2"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)


if __name__ == "__main__":
    unittest.main()