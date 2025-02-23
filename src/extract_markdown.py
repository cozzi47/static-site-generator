import re


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