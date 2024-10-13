from textnode import TextNode
from htmlnode import HTMLNode

def main():
    print("hello world")
    
    text_node = TextNode("hello world", "bold", "https://boot.dev")
    print(text_node)
    
    html_node = HTMLNode("p", "new paragraph")
    print(html_node)

if __name__ == "__main__":
    main()
