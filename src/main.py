from textnode import TextNode, TextType
from functions import *

def main():
    copy_static_to_public()
    generate_pages_recursive(dest_dir_path = "public", dir_path_content = "content", template_path = "template.html")


if __name__ == "__main__":
    main()
    