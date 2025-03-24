import os
import pathlib
from markdown_to_html_node import markdown_to_html_node


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line.lstrip("#").strip()
    raise ValueError("No h1 header found in markdown")


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    dir_contents = os.listdir(dir_path_content)
    for content in dir_contents:
        full_content_path = os.path.join(dir_path_content, content)
        
        # Create destination file path
        if os.path.isfile(full_content_path) and content.endswith(".md"):
            dest_filename = content.replace(".md", ".html")
            full_dest_path = os.path.join(dest_dir_path, dest_filename)
            print(f"Generating page from {full_content_path} to {full_dest_path} using {template_path}")
            
            # Read markdown content
            with open(full_content_path) as file:
                content_md = file.read()
            
            # Read template
            with open(template_path) as file:
                template = file.read()

            # Convert markdown to HTML
            node = markdown_to_html_node(content_md)
            html = node.to_html()
            title = extract_title(content_md)
            
            # Replace template placeholders
            template = template.replace("{{ Title }}", title)
            template = template.replace("{{ Content }}", html)
            
            # Ensure directory exists
            directory = os.path.dirname(full_dest_path)
            if directory:
                os.makedirs(directory, exist_ok=True)

            # Write output file
            with open(full_dest_path, 'w') as file:
                file.write(template)

        # Recursively process directories
        elif os.path.isdir(full_content_path):
            new_dest_dir = os.path.join(dest_dir_path, content)
            os.makedirs(new_dest_dir, exist_ok=True)  # Create subdirectory in destination
            generate_pages_recursive(full_content_path, template_path, new_dest_dir)