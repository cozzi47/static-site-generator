def markdown_to_blocks(markdown):
    markdown = markdown.strip()
    blocks = markdown.split("\n\n")
    result = []
    for block in blocks:
        if block.strip():
            lines = [line.strip() for line in block.split("\n")]
            result.append("\n".join(lines))
    return result