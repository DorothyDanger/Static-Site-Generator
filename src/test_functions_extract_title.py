import unittest
from functions import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_extract_title_valid(self):
        markdown = "# My Title\n\nSome content here."
        title = extract_title(markdown)
        self.assertEqual(title, "My Title")

    def test_extract_title_no_h1(self):
        markdown = "## Subtitle\n\nSome content here."
        with self.assertRaises(ValueError):
            extract_title(markdown)

    def test_extract_title_empty(self):
        markdown = ""
        with self.assertRaises(ValueError):
            extract_title(markdown)

    def test_extract_multiple_titles(self):
        markdown = "# First Title\n\n# Second Title"
        title = extract_title(markdown)
        self.assertEqual(title, "First Title")

    def test_extract_title_h2(self):
        markdown = "## Not a Title\n\nSome content here."
        with self.assertRaises(ValueError):
            extract_title(markdown)

    def test_extract_title_with_whitespace(self):
        markdown = "#    Title with spaces    \n\nContent."
        title = extract_title(markdown)
        self.assertEqual(title, "Title with spaces")
    
if __name__ == '__main__':
    unittest.main()