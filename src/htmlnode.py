
class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    # Child classes will override this method to render the HTML themselves
    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        if not self.props:
            return ""
        return_string = ""
        for prop in self.props:
            return_string += f' {prop}="{self.props[prop]}"'
        return return_string
    
    def __eq__(self, value):
        if not isinstance(value, HTMLNode):
            return False
        return self.tag == value.tag and self.value == value.value and self.children == value.children and self.props == value.props

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"