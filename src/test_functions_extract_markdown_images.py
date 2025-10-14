import unittest
from functions import extract_markdown_images
from textnode import TextNode

class TestFunctions(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_no_images(self):
        matches = extract_markdown_images(
            "This is text with no images."
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
            "This is text with an ![image1](https://i.imgur.com/zjjcJKZ.png) and another ![image2](http://example.org/image2.jpg)."
        )
        self.assertListEqual(
            [("image1", "https://i.imgur.com/zjjcJKZ.png"), ("image2", "http://example.org/image2.jpg")],
            matches
        )

    def test_extract_markdown_images_edge_cases(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a malformed ![image](not a url)."
        )
        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png"), ("image", "not a url")],
            matches
        )

    def test_extract_markdown_images_no_alt_text(self):
        matches = extract_markdown_images(
            "This is text with an ![](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    
if __name__ == "__main__":
    unittest.main()