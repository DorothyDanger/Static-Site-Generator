import unittest
from functions import markdown_to_blocks

class TestFunctionsMarkdownToBlocks(unittest.TestCase):
        def test_markdown_to_blocks(self):
            md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )
        
        def test_markdown_to_blocks_empty(self):
            md = ""
            blocks = markdown_to_blocks(md)
            self.assertEqual(blocks, [])
        
        def test_markdown_to_blocks_whitespace(self):
            md = "   "
            blocks = markdown_to_blocks(md)
            self.assertEqual(blocks, [])

        def test_markdown_to_blocks_single_block(self):
            md = "This is a single block of text without any double newlines."
            blocks = markdown_to_blocks(md)
            self.assertEqual(blocks, [md])

        def test_markdown_to_blocks_multiple_double_newlines(self):
            md = "Block one.\n\n\n\nBlock two after multiple newlines."
            blocks = markdown_to_blocks(md)
            self.assertEqual(blocks, ["Block one.", "Block two after multiple newlines."])

if __name__ == "__main__":
    unittest.main()