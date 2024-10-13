import unittest

from textnode import TextNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        
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

if __name__ == "__main__":
    unittest.main()