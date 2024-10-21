import os
import shutil
from generate_page import generate_page, generate_pages_recursive, generate_pages_recursive_pathlib
from recursive_copy import recursive_copy
from textnode import *
from htmlnode import HTMLNode
from textnode import text_node_to_html_node

def main():
    print("hello world")
    
    text_node = TextNode("hello world", text_type_link, "https://boot.dev")
    print(text_node)
    
    html_node = HTMLNode("p", "new paragraph")
    print(html_node)
    
    html_node_result = text_node_to_html_node(text_node)
    print(html_node_result)
    
    dir_path_static = "./static"
    dir_path_public = "./public"
    
    print("Copying static dir to public dir...")
    recursive_copy(dir_path_static, dir_path_public)
    
    print("Generating a static page")
    # generate_page("./content/index.md", "./template.html", "./public/index.html")
    # generate_pages_recursive("./content", "./template.html", "./public")
    generate_pages_recursive_pathlib("./content", "./template.html", "./public")

if __name__ == "__main__":
    main()
