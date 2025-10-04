import htmlnode

class ParentNode(htmlnode.HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode tag cannot be None")
        return_string = []
        if not self.children:
            raise ValueError("ParentNode children cannot be None")
        for child in self.children:
            return_string.append(child.to_html())
        return f"<{self.tag}{self.props_to_html()}>{''.join(return_string)}</{self.tag}>"
            

    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"