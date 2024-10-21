import os

from blocks_markdown import markdown_to_html_node

def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating a page from {from_path} to {dest_path} using {template_path}")
    try:
        with open(from_path, 'r') as markdown_file:
            markdown_content = markdown_file.read()
    except OSError as e:
        print(e)
        return
    
    try:
        with open(template_path, 'r') as template_file:
            template_content = template_file.read()
    except OSError as e:
        print(e)
        return
    
    html_node = markdown_to_html_node(markdown_content)    
    html_string = html_node.to_html()
    
    title = extract_title(markdown_content)
    print(f"Title: {title}")
    
    filled_template = template_content.replace("{{ Title }}", title)
    filled_template = filled_template.replace("{{ Content }}", html_string)
    
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    try:
        with open(dest_path, 'w') as output_file:
            output_file.write(filled_template)
    except OSError as e:
        print(e)
    
    print(f"Page generated successfuly at {dest_path}")

def extract_title(markdown: str):
    for line in markdown.split('\n'):
        if line.startswith("# "):
            return line.lstrip("# ").strip()
    
    raise Exception("No title (h1) detected")

