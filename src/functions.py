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

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    from textnode import TextNode, TextType
    from leafnode import LeafNode
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        else:
            parts = node.text.split(delimiter)
            if len(parts) % 2 == 0:
                raise Exception("Invalid markdown syntax.")
            for i in range(len(parts)):
                if parts[i] == "":
                    continue
                if i % 2 == 0:
                    new_nodes.append(TextNode(parts[i], TextType.PLAIN, None))
                else:
                    new_nodes.append(TextNode(parts[i], text_type, None))
    return new_nodes

def extract_markdown_images(text):
    import re
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    images = []
    for alt, url in matches:
        images.append((alt, url))
    return images

def extract_markdown_links(text):
    import re
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    links = []
    for anchor, url in matches:
        links.append((anchor, url))
    return links
                        
def split_nodes_image(old_nodes):
    from textnode import TextNode, TextType
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue
        else:
            full_text = node.text
            for alt, url in images:
                image = f"![{alt}]({url})"
                parts = full_text.split(image, 1)
                if len(parts) != 2:
                    raise ValueError("Invalid markdown. Image not closed.")
                if parts[0]:
                    new_nodes.append(TextNode(parts[0], TextType.PLAIN, None))
                new_nodes.append(TextNode(alt, TextType.IMAGE, url))
                full_text = parts[1]
            if full_text:
                new_nodes.append(TextNode(full_text, TextType.PLAIN, None))
    return new_nodes

def split_nodes_link(old_nodes):
    from textnode import TextNode, TextType
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue
        else:
            full_text = node.text
            for anchor, url in links:
                link = f"[{anchor}]({url})"
                parts = full_text.split(link, 1)
                if len(parts) != 2:
                    raise ValueError("Invalid markdown. Link not closed.")
                if parts[0]:
                    new_nodes.append(TextNode(parts[0], TextType.PLAIN, None))
                new_nodes.append(TextNode(anchor, TextType.LINK, url))
                full_text = parts[1]
            if full_text:
                new_nodes.append(TextNode(full_text, TextType.PLAIN, None))
    return new_nodes

def text_to_textnodes(text):
    from textnode import TextNode, TextType
    nodes = []
    nodes.append(TextNode(text, TextType.PLAIN, None))
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, '**', TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, '_', TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, '`', TextType.CODE)
    return nodes