import re
from textnode import TextNode, TextType


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if not old_nodes:
        return []
    if not isinstance(old_nodes, list):
        old_nodes = [old_nodes]
    new_nodes = []
    for node in old_nodes:
        if node.text_type is TextType.TEXT:
            text = node.text
            first_delimiter = text.find(delimiter)
            if first_delimiter == -1:
                new_nodes.append(node)
            else:
                before = text[:first_delimiter]
                second_delimiter = text.find(delimiter, first_delimiter + len(delimiter))
                if second_delimiter == -1:
                    raise Exception("No matching delimiter found.")
                between = text[first_delimiter + len(delimiter):second_delimiter]
                after = text[second_delimiter + len(delimiter):]
                if before:
                    new_nodes.append(TextNode(before, TextType.TEXT))
                if between:
                    new_nodes.append(TextNode(between, text_type))
                if after:
                    new_nodes.append(TextNode(after, TextType.TEXT))
        else:
            new_nodes.append(node)
    return new_nodes

def extract_markdown_images(text):
    extracted = []
    found = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    for alt, url in found:
        extracted.append((alt, url,))
    return extracted

def extract_markdown_links(text):
    extracted = []
    found = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    for anchor, url in found:
        extracted.append((anchor, url,))
    return extracted

def split_nodes_image(old_nodes):
    if not old_nodes:
        return []
    if not isinstance(old_nodes, list):
        old_nodes = [old_nodes]
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        extracted = extract_markdown_images(node.text)
        if not extracted:
            new_nodes.append(node)
            continue
        remaining_text = node.text
        for text, url in extracted:
            markdown_text = f"![{text}]({url})"
            parts = remaining_text.split(markdown_text, 1)
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(text, TextType.IMAGE, url))
            remaining_text = parts[1] if len(parts) > 1 else ""
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    if not old_nodes:
        return []
    if not isinstance(old_nodes, list):
        old_nodes = [old_nodes]
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        extracted = extract_markdown_links(node.text)
        if not extracted:
            new_nodes.append(node)
            continue
        remaining_text = node.text
        for text, url in extracted:
            markdown_text = f"[{text}]({url})"
            parts = remaining_text.split(markdown_text, 1)
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(text, TextType.LINK, url))
            remaining_text = parts[1] if len(parts) > 1 else ""
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes
        