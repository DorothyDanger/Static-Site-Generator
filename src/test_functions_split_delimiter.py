import unittest
from textnode import TextNode, TextType
from functions import split_nodes_delimiter

class TestFunctions(unittest.TestCase):
    def test_split_nodes_delimiter_bold(self):
        nodes = [
            TextNode("This is a **bold** text node", TextType.PLAIN),
            TextNode("This is another text node", TextType.PLAIN)
        ]
        result = split_nodes_delimiter(nodes, '**', TextType.BOLD)
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0].text, "This is a ")
        self.assertEqual(result[0].text_type, TextType.PLAIN)
        self.assertEqual(result[1].text, "bold")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, " text node")
        self.assertEqual(result[2].text_type, TextType.PLAIN)
        self.assertEqual(result[3].text, "This is another text node")
        self.assertEqual(result[3].text_type, TextType.PLAIN)

    def test_split_nodes_delimiter_no_delimiter(self):
        nodes = [
            TextNode("This is a plain text node", TextType.PLAIN)
        ]
        result = split_nodes_delimiter(nodes, '**', TextType.BOLD)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "This is a plain text node")
        self.assertEqual(result[0].text_type, TextType.PLAIN)
        
    def test_split_nodes_delimiter_unmatched_delimiter(self):
        nodes = [
            TextNode("This is a **bold text node", TextType.PLAIN)
        ]
        with self.assertRaises(Exception):
            split_nodes_delimiter(nodes, '**', TextType.BOLD)

    def test_split_nodes_delimiter_multiple(self):
        nodes = [
            TextNode("This is **bold** and **another bold** text", TextType.PLAIN)
        ]
        result = split_nodes_delimiter(nodes, '**', TextType.BOLD)
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].text, "This is ")
        self.assertEqual(result[0].text_type, TextType.PLAIN)
        self.assertEqual(result[1].text, "bold")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, " and ")
        self.assertEqual(result[2].text_type, TextType.PLAIN)
        self.assertEqual(result[3].text, "another bold")
        self.assertEqual(result[3].text_type, TextType.BOLD)
        self.assertEqual(result[4].text, " text")
        self.assertEqual(result[4].text_type, TextType.PLAIN)

    def test_split_nodes_delimiter_adjacent(self):
        nodes = [
            TextNode("This is ****bold**** text", TextType.PLAIN)
        ]
        result = split_nodes_delimiter(nodes, '**', TextType.BOLD)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This is ")
        self.assertEqual(result[0].text_type, TextType.PLAIN)
        self.assertEqual(result[1].text, "bold")
        self.assertEqual(result[1].text_type, TextType.PLAIN)
        self.assertEqual(result[2].text, " text")
        self.assertEqual(result[2].text_type, TextType.PLAIN)

    def test_split_nodes_delimiter_starts_with_delimiter(self):
        nodes = [
            TextNode("**bold** text", TextType.PLAIN)
        ]
        result = split_nodes_delimiter(nodes, '**', TextType.BOLD)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].text, "bold")
        self.assertEqual(result[0].text_type, TextType.BOLD)
        self.assertEqual(result[1].text, " text")
        self.assertEqual(result[1].text_type, TextType.PLAIN)

    def test_split_nodes_delimiter_ends_with_delimiter(self):
        nodes = [
            TextNode("text **bold**", TextType.PLAIN)
        ]
        result = split_nodes_delimiter(nodes, '**', TextType.BOLD)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].text, "text ")
        self.assertEqual(result[0].text_type, TextType.PLAIN)
        self.assertEqual(result[1].text, "bold")
        self.assertEqual(result[1].text_type, TextType.BOLD)
    
    def test_split_nodes_italic(self):
        nodes = [
            TextNode("This is _italic_ text", TextType.PLAIN)
        ]
        result = split_nodes_delimiter(nodes, '_', TextType.ITALIC)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This is ")
        self.assertEqual(result[0].text_type, TextType.PLAIN)
        self.assertEqual(result[1].text, "italic")
        self.assertEqual(result[1].text_type, TextType.ITALIC)
        self.assertEqual(result[2].text, " text")
        self.assertEqual(result[2].text_type, TextType.PLAIN)

    def test_split_nodes_code(self):
        nodes = [
            TextNode("This is `code` text", TextType.PLAIN)
        ]
        result = split_nodes_delimiter(nodes, '`', TextType.CODE)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This is ")
        self.assertEqual(result[0].text_type, TextType.PLAIN)
        self.assertEqual(result[1].text, "code")
        self.assertEqual(result[1].text_type, TextType.CODE)
        self.assertEqual(result[2].text, " text")
        self.assertEqual(result[2].text_type, TextType.PLAIN)

    def test_split_nodes_mixed(self):
        nodes = [
            TextNode("This is **bold** and _italic_ and `code` text", TextType.PLAIN)
        ]
        result = split_nodes_delimiter(nodes, '**', TextType.BOLD)
        result = split_nodes_delimiter(result, '_', TextType.ITALIC)
        result = split_nodes_delimiter(result, '`', TextType.CODE)
        self.assertEqual(len(result), 7)
        self.assertEqual(result[0].text, "This is ")
        self.assertEqual(result[0].text_type, TextType.PLAIN)
        self.assertEqual(result[1].text, "bold")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, " and ")
        self.assertEqual(result[2].text_type, TextType.PLAIN)
        self.assertEqual(result[3].text, "italic")
        self.assertEqual(result[3].text_type, TextType.ITALIC)
        self.assertEqual(result[4].text, " and ")
        self.assertEqual(result[4].text_type, TextType.PLAIN)
        self.assertEqual(result[5].text, "code")
        self.assertEqual(result[5].text_type, TextType.CODE)
        self.assertEqual(result[6].text, " text")
        self.assertEqual(result[6].text_type, TextType.PLAIN)

if __name__ == "__main__":
    unittest.main()