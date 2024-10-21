import os
from pathlib import Path

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

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str):
    for filename in os.listdir(dir_path_content):
        source_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        
        if os.path.isdir(source_path):
            os.makedirs(dest_path, exist_ok=True)
            generate_pages_recursive(source_path, template_path, dest_path)
        elif os.path.isfile(source_path) and source_path.endswith(".md"):
            with open(source_path, 'r') as md_file:
                md_content = md_file.read()
            
            with open(template_path, 'r') as tmpl_file:
                tmpl_content = tmpl_file.read()
            
            output_name = os.path.basename(source_path)
            
            html_content = generate_page(md_content, tmpl_content, output_name)
            
            if html_content:
                dest_html_path = os.path.splitext(dest_path)[0] + ".html"
                os.makedirs(os.path.dirname(dest_html_path), exist_ok=True)
                
                with open(dest_html_path, 'w') as html_file:
                    html_file.write(html_content)
        else:
            print(f"Nothing to generate for {filename}")
            
    pass

def generate_pages_recursive_pathlib(dir_path_content: str, template_path: str, dest_dir_path: str):
    content_path = Path(dir_path_content)
    tmpl_path = Path(template_path)
    dest_path = Path(dest_dir_path)
    
    for item in content_path.iterdir():
        
        if item.is_dir():
            generate_pages_recursive_pathlib(str(item), str(tmpl_path), str(dest_path))
        elif item.is_file() and item.suffix == ".md":
            relative_path = item.relative_to(content_path)
            item_dest = dest_path / relative_path.with_suffix(".html")
            item_dest.parent.mkdir(parents=True, exist_ok=True)
            
            generate_page(str(item), str(tmpl_path), str(item_dest))
    