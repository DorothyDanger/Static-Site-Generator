import unittest
from functions import extract_markdown_links
from textnode import TextNode

class TestFunctions(unittest.TestCase):
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://example.com) and another [link2](http://example.org)."
        )
        self.assertListEqual(
            [("link", "https://example.com"), ("link2", "http://example.org")],
            matches
        )

    def test_extract_markdown_links_no_links(self):
        matches = extract_markdown_links(
            "This is text with no links."
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_links_with_image(self):
        matches = extract_markdown_links(
            "This is text with a ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://example.com)."
        )
        self.assertListEqual(
            [("link", "https://example.com")],
            matches
        )

    def test_extract_markdown_links_edge_cases(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://example.com) and a malformed [link](not a url)."
        )
        self.assertListEqual(
            [("link", "https://example.com"), ("link", "not a url")],
            matches
        )

if __name__ == "__main__":
    unittest.main()