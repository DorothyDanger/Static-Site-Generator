def text_node_to_html_node(text_node):
    from textnode import TextType
    from leafnode import LeafNode


    match (text_node.text_type):
        case TextType.PLAIN:
            # Just return the text as is, no wrapping
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            # Wrap in <b> tags
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            # Wrap in <i> tags
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            # Wrap in <code> tags
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            # Wrap in <a> tags with href attribute
            if text_node.url is None:
                raise ValueError("Must have URL for link")
            return LeafNode("a", text_node.text, f'"href"= {text_node.url}')
        case TextType.IMAGE:
            # Wrap in <img> tags with src attribute, no inner text
            if text_node.url is None:
                raise ValueError("Must have URL for image")
            return LeafNode("img", "", f'"src"= {text_node.url}, alt="{text_node.text}"')
        
        case _:
            # Default to plain text if type is unrecognized
            return LeafNode(None, text_node.text)