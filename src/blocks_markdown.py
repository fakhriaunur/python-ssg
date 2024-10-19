from typing import List
from htmlnode import HTMLNode
from inline_markdown import text_to_textnodes
from leafnode import LeafNode
from textnode import *
from parentnode import ParentNode

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_olist = "ordered_list"
block_type_ulist = "unordered_list"

def markdown_to_blocks(markdown: str) -> List[str]:
    blocks = markdown.split("\n\n")
    return list(filter(None, map(str.strip, blocks)))
    # filtered_blocks = []
    # for block in blocks:
    #     if not block:
    #         continue
    #     stripped_block = block.strip()
    #     filtered_blocks.append(stripped_block)
    # return filtered_blocks

def block_to_block_type(markdown: str) -> str:
    lines = markdown.split("\n")
    first_line = lines[0]
    
    pound_count = first_line.count("#", 0, 6)
    if 1 <= pound_count <= 6 and first_line[pound_count] == " ":
        return "heading"
    
    if lines[0].startswith("```") and lines[-1].endswith("```"):
        return "code"
    
    if all(line.startswith(">") for line in lines):
        return "quote"
    
    if all(line.startswith("*") or line.startswith("-") for line in lines):
        return "unordered_list"
    
    if all(line.strip() for line in lines):
        current_numbering = 1
        for line in lines:
            parts = line.split(".", 1)
            if len(parts) != 2:
                return "paragraph"
            
            number_part, rest = parts
            
            if not number_part.strip().isdigit():
                return "paragrah"
            
            if int(number_part) != current_numbering:
                return "paragraph"
            
            if not rest.startswith(" "):
                return "paragraph"
            
            current_numbering += 1
        
        return "ordered_list"
    
    return "paragraph"

def markdown_to_html_node(markdown: str):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    
    return ParentNode("div", children, None)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == block_type_paragraph:
        return paragraph_to_html_node(block)
    
    if block_type == block_type_heading:
        return heading_to_html_node(block)
    
    if block_type == block_type_code:
        return code_to_html_node(block)
    
    if block_type == block_type_quote:
        return quote_to_html_node(block)
    
    if block_type == block_type_olist:
        return ulist_to_html_node(block)
    
    if block_type == block_type_ulist:
        return olist_to_html_node(block)
    
    raise ValueError(f"Invalid block_type {block_type}")

def text_to_children(text: str):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    
    return children 

def paragraph_to_html_node(block: str):
    lines = block.split('\n')
    paragraph = ' '.join(lines)
    children = text_to_children(paragraph)
    
    return ParentNode("p", children)

def heading_to_html_node(block: str):
    level = 0
    for char in block:
        if char == '#':
            level += 1
        else:
            break
    
    if level + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {level}")
    
    text = block[level + 1:]
    children = text_to_children(text)
    
    return ParentNode(f"h{level}", children)
    

def code_to_html_node(block: str):
    if not (
        block.startswith("```") and block.endswith("```")
    ):
        raise ValueError("Invalid code block")
    
    text = block[4:-3]
    children = text_to_children(text)
    code = ParentNode("code", children)
    
    return ParentNode("pre", [code])

def olist_to_html_node(block: str):
    items = block.split('\n')
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    
    return ParentNode("ol", html_items)

def ulist_to_html_node(block: str):
    items = block.split('\n')
    html_items = []
    
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    
    return ParentNode("ul", html_items)

def quote_to_html_node(block: str):
    lines = block.split('\n')
    new_lines = []
    for line in lines:
        if not line.startswith('>'):
            raise ValueError("Invalid quote block")
        
        new_lines.append(line.lstrip('>').strip())
    
    content = ' '.join(new_lines)
    children = text_to_children(content)
    
    return ParentNode("blockquote", children)
    

# def markdown_to_html_node(markdown: str) -> HTMLNode:
#     blocks = markdown_to_blocks(markdown)
#     parent_node = HTMLNode("div")
#     for block in blocks:
#         block_type = block_to_block_type(block)
#         block_node = create_block_node(block_type, block)
        
#         if block_type in ["paragraph", "heading"]:
#             block_node.children.extend(text_to_children(block))
#         elif block_type in ["unordered_list", "ordered_list"]:
#             list_items = block.split('\n')
#             for item in list_items:
#                 li_node = HTMLNode("li")
#                 li_node.children.extend(text_to_children(item.lstrip("- ")))
#                 block_node.children.append(li_node)
#         elif block_type == "code":
#             block_node.children.append(HTMLNode(None, block))
#         elif block_type == "quote":
#             block_node.children.extend(text_to_children(block.lstrip("> ")))
        
#         parent_node.children.append(block_node)
#         # current_node = parent_node
#         # for tag in tags:
#         #     new_node = HTMLNode(tag)
#         #     current_node.children.append(new_node)
#         #     current_node = new_node
        
#         # current_node.children.extend(text_to_children(block))
        
#     return parent_node

# def create_block_node(block_type: str, block_content: str):
#     if block_type == "heading":
#         level = block_content.count('#')
#         # level = len(block_content.split()[0])
#         return HTMLNode(f"h{level}")
    
#     if block_type == "paragraph":
#         return HTMLNode("p")
    
#     if block_type == "code":
#         return HTMLNode("pre",children=[HTMLNode("code")])
    
#     if block_type == "unordered_list":
#         return HTMLNode("ul")
    
#     if block_type == "ordered_list":
#         return HTMLNode("ol")
    
#     if block_type == "quote":
#         return HTMLNode("blockquote")
    
#     raise ValueError(f"Unknown block type: {block_type}")

# def text_to_children(text: str) -> List[HTMLNode]:
#     text_node = TextNode("text", text_type_text)
#     leaf_node = text_node_to_html_node(text_node)
    
#     if isinstance(leaf_node, TextNode):
#         if leaf_node.text_type == text_type_text:
#             return [HTMLNode(None, leaf_node.text)]
        
#         if leaf_node.text_type == text_type_bold:
#             return [HTMLNode("b", leaf_node.text)]
        
#         if leaf_node.text_type == text_type_italic:
#             return [HTMLNode("i", leaf_node.text)]
        
#         if leaf_node.text_type == text_type_code:
#             return [HTMLNode("code", leaf_node.text)]
        
#         if leaf_node.text_type == text_type_link:
#             return [HTMLNode("a", leaf_node.text, {"href": leaf_node.url})]
        
#         if leaf_node.text_type == text_type_image:
#             return [HTMLNode("img", "", {"src": leaf_node.url, "alt": leaf_node.text})]
    
#     else:
#         raise ValueError(f"Unknown leaf node type: {type(leaf_node)}")
            