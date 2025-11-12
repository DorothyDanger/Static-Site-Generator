import unittest
from functions import markdown_to_html_node

class TestFunctionsMarkdownToHtmlNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading(self):
        md = "# This is a Heading 1\n\n## This is a Heading 2 with **bold** text\n"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a Heading 1</h1><h2>This is a Heading 2 with <b>bold</b> text</h2></div>",
        )

    def test_unordered_list(self):
        md = " - Item 1\n- Item 2 with _italic_\n- Item 3 with `code`\n"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item 1</li><li>Item 2 with <i>italic</i></li><li>Item 3 with <code>code</code></li></ul></div>",
        )

    def test_ordered_list(self):
        md = "1. First item\n2. Second item with **bold**\n3. Third item with `code`\n"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second item with <b>bold</b></li><li>Third item with <code>code</code></li></ol></div>",
        )

    def test_mixed_content(self):
        md = " # Heading\n\nThis is a paragraph with **bold** text.\n\n- List item 1\n- List item 2 with _italic_\n\n```\nCode block here\n``` \n"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading</h1><p>This is a paragraph with <b>bold</b> text.</p><ul><li>List item 1</li><li>List item 2 with <i>italic</i></li></ul><pre><code>Code block here\n</code></pre></div>",
        )

    
if __name__ == "__main__":
    unittest.main()