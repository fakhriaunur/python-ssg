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

if __name__ == "__main__":
    main()
