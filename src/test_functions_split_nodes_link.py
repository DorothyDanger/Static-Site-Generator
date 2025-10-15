import unittest
from textnode import TextNode, TextType
from functions import split_nodes_link

class TestFunctions(unittest.TestCase):
    def test_split_nodes_link(self):
        nodes = [
            TextNode("This is a [link](https://example.com) in a text node", TextType.PLAIN),
            TextNode("This is another text node", TextType.PLAIN)
        ]
        result = split_nodes_link(nodes)
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0].text, "This is a ")
        self.assertEqual(result[0].text_type, TextType.PLAIN)
        self.assertEqual(result[1].text, "link")
        self.assertEqual(result[1].text_type, TextType.LINK)
        self.assertEqual(result[1].url, "https://example.com")
        self.assertEqual(result[2].text, " in a text node")
        self.assertEqual(result[2].text_type, TextType.PLAIN)
        self.assertEqual(result[3].text, "This is another text node")
        self.assertEqual(result[3].text_type, TextType.PLAIN)

    def test_split_nodes_link_no_link(self):
        nodes = [
            TextNode("This is a plain text node", TextType.PLAIN)
        ]
        result = split_nodes_link(nodes)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "This is a plain text node")
        self.assertEqual(result[0].text_type, TextType.PLAIN)

    def test_split_nodes_link_multiple(self):
        nodes = [
            TextNode("This is a [link1](https://example.com) and another [link2](http://example.org) in one text node", TextType.PLAIN)
        ]
        result = split_nodes_link(nodes)
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].text, "This is a ")
        self.assertEqual(result[0].text_type, TextType.PLAIN)
        self.assertEqual(result[1].text, "link1")
        self.assertEqual(result[1].text_type, TextType.LINK)
        self.assertEqual(result[1].url, "https://example.com")
        self.assertEqual(result[2].text, " and another ")
        self.assertEqual(result[2].text_type, TextType.PLAIN)
        self.assertEqual(result[3].text, "link2")
        self.assertEqual(result[3].text_type, TextType.LINK)
        self.assertEqual(result[3].url, "http://example.org")
        self.assertEqual(result[4].text, " in one text node")
        self.assertEqual(result[4].text_type, TextType.PLAIN)

    def test_split_nodes_link_adjacent(self):
        nodes = [
            TextNode("This is a [link1](https://example.com)[link2](http://example.org) in one text node", TextType.PLAIN)
        ]
        result = split_nodes_link(nodes)
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0].text, "This is a ")
        self.assertEqual(result[0].text_type, TextType.PLAIN)
        self.assertEqual(result[1].text, "link1")
        self.assertEqual(result[1].text_type, TextType.LINK)
        self.assertEqual(result[1].url, "https://example.com")
        self.assertEqual(result[2].text, "link2")
        self.assertEqual(result[2].text_type, TextType.LINK)
        self.assertEqual(result[2].url, "http://example.org")
        self.assertEqual(result[3].text, " in one text node")
        self.assertEqual(result[3].text_type, TextType.PLAIN)
    
if __name__ == "__main__":
    unittest.main()