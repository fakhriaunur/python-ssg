import re
from typing import List
from textnode import *



def split_nodes_delimiter(old_nodes, delimiter, text_type):
    print(f"Processing nodes: {old_nodes}")
    print(f"Delimiter: {delimiter}")
    print(f"Text type: {text_type}")
    
    def custom_split(text: str, delimiter: str):
        result = []
        current = ""
        in_brackets = False
        i = 0
        
        while i < len(text):
            if (
                text[i: i + len(delimiter)] == delimiter and
                not in_brackets and
                (i == 0 or not text[i-1].isalnum()) and
                (i + len(delimiter) == len(text) or not
                text[i+len(delimiter)].isalnum()) and
                (i == 0 or text[i-1] != "\\")
            ):
                j = i + len(delimiter)
                while j < len(text) and text[j:j+len(delimiter)] == delimiter:
                    j += len(delimiter)
                
                if current:
                    result.append(current)
                result.append(text[i:j])
                current = ""
                i = j
            else:
                if text[i] == '[':
                    in_brackets = True
                elif text[i] == ']':
                    in_brackets = False
                
                current += text[i]
                i += 1
        
        if current:
            result.append(current)
        
        return result
        
    new_nodes = []

    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        
        splitted_nodes = []
        sections = custom_split(node.text, delimiter)
        print(f"Sections: {sections}")
        if len(sections) % 2 == 0:
            raise Exception("Invalid Markdown syntax, formatted section is not closed")
        
        for i, chunk in enumerate(sections):
            if chunk == "":
                continue
            
            if i % 2 == 0:
                splitted_nodes.append(TextNode(chunk, text_type_text))
            else:
                splitted_nodes.append(TextNode(chunk, text_type))
        
        new_nodes.extend(splitted_nodes)

    print(f"Returning nodes: {new_nodes}")
    return new_nodes

def extract_markdown_images(text: str):
    images_pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(images_pattern, text)
    return matches

def extract_markdown_links(text: str):
    links_pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(links_pattern, text)
    return matches

def split_nodes_image(old_nodes: List[TextNode]):
    new_nodes = []
    
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        
        links = extract_markdown_images(old_node.text)
        if not links:
            new_nodes.append(old_node)
            continue
        
        remaining_text = old_node.text
        for alt_text, url in links:
            images = remaining_text.split(f"![{alt_text}]({url})", 1)
            if images[0]:
                new_nodes.append(TextNode(images[0], text_type_text))
            new_nodes.append(TextNode(alt_text, text_type_image, url))
            
            if len(images) > 1:
                remaining_text = images[1]
            else:
                remaining_text = ""
            
            if remaining_text:
                new_nodes.append(TextNode(images[1], text_type_text))
        
    return new_nodes

def split_nodes_link(old_nodes: List[TextNode]):
    new_nodes = []
    
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        
        links = extract_markdown_links(old_node.text)
        if not links:
            new_nodes.append(old_node)
            continue
        
        remaining_text = old_node.text
        for link_text, url in links:
            sections = remaining_text.split(f"[{link_text}]({url})", 1)
            
            if sections[0]:
                new_nodes.append(TextNode(sections[0], text_type_text))
            new_nodes.append(TextNode(link_text, text_type_link, url))
            
            if len(sections) > 1:
                remaining_text = sections[1]
            else:
                remaining_text = ""
            
            if remaining_text:
                new_nodes.append(TextNode(remaining_text, text_type_text))
    
    return new_nodes

def text_to_textnodes(text: str):
    nodes = [TextNode(text, text_type_text)]
    
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    return nodes