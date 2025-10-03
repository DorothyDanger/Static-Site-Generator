import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("div", "This is a div", None, None)
        node2 = HTMLNode("div", "This is a div", None, None)
        self.assertEqual(node, node2)
    
    def test_not_eq(self):
        node = HTMLNode("div", "This is a div", None, None)
        node2 = HTMLNode("span", "This is not a div", None, None)
        self.assertNotEqual(node, node2)

    def test_not_instance(self):
        node = HTMLNode("div", "This is a div", None, None)
        self.assertNotEqual(node, "This is not a div")

    def test_repr(self):
        node = HTMLNode("div", "This is a div", None, None)
        self.assertEqual(repr(node), "HTMLNode(div, This is a div, None, None)")
        
if __name__ == "__main__":
    unittest.main()