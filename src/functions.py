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

def markdown_to_blocks(markdown):
    lines = markdown.split('\n\n')
    blocks = []
    for line in lines:
        multiple_lines = line.strip().split('\n')
        stripped = ""
        #if len(multiple_lines) > 1:
        for i in range(len(multiple_lines)):
            if i == len(multiple_lines) - 1:
                stripped += multiple_lines[i].strip()
            else:
                stripped += multiple_lines[i].strip() + '\n'
        #else:
            #stripped = line.strip()
        if stripped:
            blocks.append(stripped)
    return blocks

from enum import Enum
class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    import re
    lines = block.split("\n")

    if re.match(r"#{1,6} ", lines[0]):
        return BlockType.HEADING
    elif re.match(r"```.*?", lines[0]):
        if re.match(r".*?```", lines[-1]):
            return BlockType.CODE
        else:
            return BlockType.PARAGRAPH
    elif re.match(r"> ", lines[0]):
        return BlockType.QUOTE
    elif re.match(r"- .*?", lines[0]):
        for line in lines:
            if not re.match(r"- .*?", line):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    elif re.match(r"\d. .*?", lines[0]):
        for line in lines:
            if not re.match(r"\d. .*?", line):
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
    

def markdown_to_html_node(markdown):
    from htmlnode import HTMLNode
    from leafnode import LeafNode
    from parentnode import ParentNode
    # So. In reading through the pseudocode I need to create multiple helper functions.
    # These will be used to convert each block to its respective HTMLNode representation.
    # Within the helper functions I will need to make use of other functions I've written.
    # For instance if something is a "PARAGRAPH", it can still contain bold, italic, links, images, etc.
    # So I will need to use text_to_textnodes within those helper functions.
    # But it needs to be altered to wrap in <p>, <h1>, <ol>, <ul>, <li>, etc.
    # I imagine I will have an additional helper function for these other helper functions.
    # A helper helper function. Which will cdo this wrapping.
    # e.g. the BlockType.PARAGRAPH function will convert each item in the block to whichever respective textnode it is.
    # Then i will loop through them and have a new "helper helper function" that will convert a "BOLD textnode" to a "<b>HTMLNode</b>".
    # for ITALIC, LINK, IMAGE, CODE, PLAIN, etc.
    # Now that I've worked through the logic I will implement it tomorrow and reference back here as needed.
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        block_node = block_and_type_to_html_node(block, block_type)
        block_nodes.append(block_node)
    # This stuff does not work. I think I'm overthinking the implementation.
    # My helper functions should only return leaf nodes. None of them should have children.
    # I simply need to do string formatting and wrap them in tags.
    # ABOVE IS THE MOST IMPORTANT
    # In my tiredness, I do believe I simply have to create loops and make a leaf node list for each
    # Then return a parent node with the list as the child. TRUE!!!
    div_parent = ParentNode("div", block_nodes, None)
    return div_parent

def block_and_type_to_html_node(block, block_type):
    match (block_type):
            case BlockType.PARAGRAPH:
                return paragraph_block_to_html_node(block)
            case BlockType.HEADING:
                return heading_block_to_html_node(block)
            case BlockType.CODE:
                return code_block_to_html_node(block)
            case BlockType.QUOTE:
                return quote_block_to_html_node(block)
            case BlockType.UNORDERED_LIST:
                return unordered_list_block_to_html_node(block)
            case BlockType.ORDERED_LIST:
                return ordered_list_block_to_html_node(block)
            case _:
                raise ValueError("Unrecognized block type")

def paragraph_block_to_html_node(block):
    from htmlnode import HTMLNode
    from leafnode import LeafNode
    from parentnode import ParentNode
    #block = block.strip("\n")
    #text_nodes = text_to_textnodes(block)
    #children = []
    #for text_node in text_nodes:
        #html_node = text_node_to_html_node(text_node)
        #children.append(html_node)
    text_nodes = text_to_textnodes(block)
    children = []
    for tn in text_nodes:
        tn.text = tn.text.replace('\n', ' ')
        html_node = text_node_to_html_node(tn)
        children.append(html_node)
    paragraph_node = ParentNode("p", children, None)
    return paragraph_node

def heading_block_to_html_node(block):
    from htmlnode import HTMLNode
    from leafnode import LeafNode
    from parentnode import ParentNode
    import re

    match = re.match(r"(#{1,6}) (.*)", block)
    total_hashes = len(match.group(1))
    heading_text = match.group(2)

    match total_hashes:
        case 1:
            tag = "h1"
        case 2:
            tag = "h2"
        case 3:
            tag = "h3"
        case 4:
            tag = "h4"
        case 5:
            tag = "h5"
        case 6:
            tag = "h6"
    text_node = text_to_textnodes(heading_text)
    # Get full text including inline formatting
    full_text = ""
    for tn in text_node:
        full_text += text_node_to_html_node(tn).to_html()

    heading_node = LeafNode(tag, full_text, None)
    return heading_node

def code_block_to_html_node(block):
    from leafnode import LeafNode
    from parentnode import ParentNode
    # This worked
    #code_text = ""
    #block = block.strip("```").strip()
    #for line in block.split("\n"):
        #code_text += line + "\n"
    #code_text.strip()

    #code_text = block.strip("```").strip() This single line worked before but didn't preserve the final newline
    #code_text = code_text.rstrip("\n")
    #print(f"code text: {code_text}")

    code_text = block.strip("```").strip() + "\n" # After tinkering around with the above I realised I could just do this.
    code_node = LeafNode("code", code_text)
    pre_node = ParentNode("pre", [code_node], None)
    return pre_node

def quote_block_to_html_node(block):
    from htmlnode import HTMLNode
    from leafnode import LeafNode
    quote_text = block.lstrip("> ").strip()
    #text_nodes = text_to_textnodes(quote_text)
    #hildren = []
    #for text_node in text_nodes:
        #html_node = text_node_to_html_node(text_node)
        #children.append(html_node)
    quote_node = LeafNode("blockquote", quote_text)
    return quote_node

def unordered_list_block_to_html_node(block):
    from htmlnode import HTMLNode
    from leafnode import LeafNode
    from parentnode import ParentNode
    lines = block.strip().split("\n")
    list_nodes = []
    for line in lines:
        text = line.lstrip("- ").strip()
        text_node = text_to_textnodes(text)
        list_text = ""
        # Handles inline formatting for the text
        for tn in text_node:
            list_text += text_node_to_html_node(tn).to_html()
        li_node = LeafNode("li", list_text, None)
        list_nodes.append(li_node)
    ul_node = ParentNode("ul", list_nodes, None)
    return ul_node

def ordered_list_block_to_html_node(block):
    from htmlnode import HTMLNode
    from leafnode import LeafNode
    from parentnode import ParentNode
    lines = block.strip().split("\n")
    list_nodes = []
    for line in lines:
        text = line.lstrip("0123456789. ").strip()
        text_node = text_to_textnodes(text)
        list_text = ""
        for tn in text_node:
            list_text += text_node_to_html_node(tn).to_html()
        li_node = LeafNode("li", list_text, None)
        list_nodes.append(li_node)
    ol_node = ParentNode("ol", list_nodes, None)
    return ol_node

# Recursive function to copy static files to public directory
def copy_static_to_public(source = "static", destination = "public"):
    #Write a recursive function that copies all the contents from a source directory to a destination directory (in our case, static to public)
    #It should first delete all the contents of the destination directory (public) to ensure that the copy is clean.
    #It should copy all files and subdirectories, nested files, etc.
    #I recommend logging the path of each file you copy, so you can see what's happening as you run and debug your code.
    import os
    import shutil

    source_directory = source
    destination_directory = destination
    # Delete all contents of destination
    if os.path.exists(destination_directory):
        shutil.rmtree(destination_directory)
    os.mkdir(destination_directory)

    # Copy contents from source to destination
    for item in os.listdir(source_directory):
        source_path = os.path.join(source_directory, item)
        destination_path = os.path.join(destination_directory, item)
        if os.path.isfile(source_path):
            shutil.copy(source_path, destination_path)
            print(f"Copied file: {source_path} to {destination_path}")
        else:
            copy_static_to_public(source_path, destination_path)

def extract_title(markdown):
    import re
    lines = markdown.split("\n")#
    for line in lines:
        match = re.match(r"# (.*)", line)
        if match:
            return match.group(1).strip()
    raise ValueError("No H1 header found; invalid markdown format.")


    

    
