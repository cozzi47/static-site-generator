from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
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