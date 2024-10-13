import unittest

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_link,
    text_type_image
)

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node",text_type_bold)
        node2 = TextNode("This is a text node",text_type_bold)
        
        self.assertEqual(node, node2)
    
    def test_eq2(self):
        node = TextNode("This is a text node", "bold")
        node3 = TextNode("This is a text node", "bold", "https://boot.dev")
        self.assertNotEqual(node, node3)
    
    def test_eq3(self):
        node = TextNode("This is a text node", "bold")
        node4 = TextNode("This is a text node", "italic")
        self.assertNotEqual(node, node4)
        
    def test_eq_repr(self):
        node = TextNode("This is a text node", "bold", "https://boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, bold, https://boot.dev)", repr(node)
        )
    
    def test_eq_textnode_to_htmlnode(self):
        pass

if __name__ == "__main__":
    unittest.main()