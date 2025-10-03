import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    def test_not_eq_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, "This is a different text node")
    def test_url_eq(self):
        node = TextNode("This is a text node", TextType.LINK, "http://example.com")
        node2 = TextNode("This is a text node", TextType.LINK, "http://example.com")
        self.assertEqual(node, node2)
    def test_url_not_eq(self):
        node = TextNode("This is a text node", TextType.LINK, "http://example.com")
        node2 = TextNode("This is a text node", TextType.LINK, "http://different.com")
        self.assertNotEqual(node, node2)
    def test_url_none_not_eq(self):
        node = TextNode("This is a text node", TextType.LINK, "http://example.com")
        node2 = TextNode("This is a text node", TextType.LINK, None)
        self.assertNotEqual(node, node2)
    def test_text_type_property_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node.text_type, TextType.BOLD)
    def test_text_type_property_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node.text_type, TextType.ITALIC)
if __name__ == "__main__":
    unittest.main()