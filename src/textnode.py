from enum import Enum

class TextType(Enum):
    PLAIN = "plain"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text: str, text_type, url: str = None):
        self.text = text
        self.url = url

        match text_type:
            case TextType.PLAIN:
                self.text_type = text_type
            case TextType.BOLD:
                self.text_type = text_type
            case TextType.ITALIC:
                self.text_type = text_type
            case TextType.CODE:
                self.text_type = text_type
            case TextType.LINK:
                self.text_type = text_type
            case TextType.IMAGE:
                self.text_type = text_type
            #default to plain if not recognized
            case _:
                self.text_type = TextType.PLAIN
        

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

    
    
    def __eq__(self, value):
        if not isinstance(value, TextNode):
            return False
        return self.text == value.text and self.text_type == value.text_type and self.url == value.url