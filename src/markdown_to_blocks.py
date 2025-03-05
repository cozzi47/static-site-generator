import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE ="quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    markdown = markdown.strip()
    blocks = markdown.split("\n\n")
    result = []
    for block in blocks:
        if block.strip():
            if block.startswith("```"):
                result.append(block)
            else:
                lines = [line.strip() for line in block.split("\n")]
                result.append("\n".join(lines))
    return result

def block_to_block_type(block):
    lines = block.split("\n")
    heading = re.findall(r"^#{1,6} ", block)
    if heading:
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    ordered_list = True
    for i, line in enumerate(lines):
        if not re.match(f"^{i+1}\\. ", line):
            ordered_list = False
            break
    if ordered_list and lines:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH