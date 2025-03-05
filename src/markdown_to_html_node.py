from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode import TextNode, TextType
from markdown_to_textnode import text_to_textnodes
from markdown_to_blocks import markdown_to_blocks, block_to_block_type, BlockType


def markdown_to_html_node(markdown):
    html_node = ParentNode("div", [])
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if not block.strip():
            continue
        block_type = block_to_block_type(block)
        tag = block_type_to_tag(block, block_type)
        if not tag:
            raise ValueError(f"Invalid block type or tag for: {block}")
        
        if block_type == BlockType.CODE:
            child_node = process_code_block(block)
            if child_node:
                html_node.add_child(child_node)

        elif block_type == BlockType.ORDERED_LIST:
            child_node = process_ordered_list(block)
            html_node.add_child(child_node)

        elif block_type == BlockType.UNORDERED_LIST:
            child_node = process_unordered_list(block)
            html_node.add_child(child_node)

        else:
            child_node = HTMLNode(tag)
            text_nodes = text_to_textnodes(block)
            for text_node in text_nodes:
                child_node.add_child(text_node.text_node_to_html_node())
            html_node.add_child(child_node)
                
    return html_node


def process_code_block(block):
    lines =  block.split("\n")
    inner_content = "\n".join(lines[1:-1])
    if not inner_content.strip():  # If the content is essentially empty
        inner_content = " "
    code_node = LeafNode("code", inner_content)
    child_node = HTMLNode("pre")
    child_node.add_child(code_node)
    return child_node


def process_ordered_list(block):
    lines = block.split("\n")
    ol_node = HTMLNode("ol")
    for line in lines:
        line = line.strip()
        if line:
            content = line.split(". ", 1)[-1].strip()
            li_node = LeafNode("li", content)
            ol_node.add_child(li_node)
    return ol_node


def process_unordered_list(block):
    lines = block.split("\n")
    ul_node = HTMLNode("ul")
    for line in lines:
        line = line.strip()
        if line:
            content = line[2:].strip() if line.startswith(("-", "*")) else line
            li_node = LeafNode("li", content)
            ul_node.add_child(li_node)
    return ul_node


def block_type_to_tag(block, block_type):
    match block_type:
        case BlockType.HEADING:
            if block.startswith("# "):
                return "h1"
            if block.startswith("## "):
                return "h2"
            if block.startswith("### "):
                return "h3"
            if block.startswith("#### "):
                return "h4"
            if block.startswith("##### "):
                return "h5"
            if block.startswith("###### "):
                return "h6"
        case BlockType.CODE:
            return "code"
        case BlockType.QUOTE:
            return "blockquote"
        case BlockType.UNORDERED_LIST:
            return "ul"
        case BlockType.ORDERED_LIST:
            return "ol"
        case _:
            return "p"

