import unittest
from textnode import TextNode, TextType
from functions import text_to_textnodes

class TestFunctions(unittest.TestCase):
    def test_text_to_textnodes_plain(self):
        text = "This is a plain text."
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, text)
        self.assertEqual(nodes[0].text_type, TextType.PLAIN)

    def test_text_to_textnodes_empty(self):
        text = ""
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 0)
        

    def test_text_to_textnodes_whitespace(self):
        text = "   "
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "   ")
        self.assertEqual(nodes[0].text_type, TextType.PLAIN)

    def test_text_to_textnodes_all_options(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)

        self.assertListEqual(nodes, [
    TextNode("This is ", TextType.PLAIN),
    TextNode("text", TextType.BOLD),
    TextNode(" with an ", TextType.PLAIN),
    TextNode("italic", TextType.ITALIC),
    TextNode(" word and a ", TextType.PLAIN),
    TextNode("code block", TextType.CODE),
    TextNode(" and an ", TextType.PLAIN),
    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
    TextNode(" and a ", TextType.PLAIN),
    TextNode("link", TextType.LINK, "https://boot.dev"),])
        
    def test_text_to_textnodes_unmatched_delimiters(self):
        text = "This is **bold text with no closing delimiter"
        with self.assertRaises(Exception):
            text_to_textnodes(text)
        text = "This is _italic text with no closing delimiter"
        with self.assertRaises(Exception):
            text_to_textnodes(text)
        text = "This is `code text with no closing delimiter"
        with self.assertRaises(Exception):
            text_to_textnodes(text)
    
    def test_text_to_textnodes_multiple_same_delimiters(self):
        text = "This is **bold** and **another bold** text"
        nodes = text_to_textnodes(text)
        self.assertListEqual(nodes, [
            TextNode("This is ", TextType.PLAIN),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.PLAIN),
            TextNode("another bold", TextType.BOLD),
            TextNode(" text", TextType.PLAIN),
        ])

    def test_text_to_textnodes_unended_image(self):
        text = "This is an ![image]( and some text"
        nodes = text_to_textnodes(text)
        self.assertListEqual(nodes, [
            TextNode("This is an ![image]( and some text", TextType.PLAIN),
        ])