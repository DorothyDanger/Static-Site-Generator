import unittest
from leafnode import LeafNode
from parentnode import ParentNode

class TestParentNode(unittest.TestCase):
    def test_parent_to_html(self):
        child1 = LeafNode("p", "Hello, world!")
        child2 = LeafNode("a", "Click here", {"href": "http://example.com"})
        parent = ParentNode("div", [child1, child2], {"class": "container"})
        expected_html = '<div class="container"><p>Hello, world!</p><a href="http://example.com">Click here</a></div>'
        self.assertEqual(parent.to_html(), expected_html)
    
    def test_parent_no_children(self):
        parent = ParentNode("div", [], {"class": "empty"})
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_parent_no_tag(self):
        child1 = LeafNode("p", "Hello, world!")
        parent = ParentNode(None, [child1], {"class": "no-tag"})
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_parent_not_eq(self):
        child1 = LeafNode("p", "Hello, world!")
        parent1 = ParentNode("div", [child1], {"class": "container"})
        parent2 = ParentNode("div", [child1], {"class": "different"})
        self.assertNotEqual(parent1, parent2)

    def test_parent_child_no_value(self):
        child1 = LeafNode("p", None)
        parent = ParentNode("div", [child1], {"class": "container"})
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_multiple_children(self):
        child_node1 = LeafNode("span", "child1")
        child_node2 = LeafNode("span", "child2")
        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(parent_node.to_html(), "<div><span>child1</span><span>child2</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )


if __name__ == "__main__":
    unittest.main()

    