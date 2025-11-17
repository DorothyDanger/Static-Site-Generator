from textnode import TextNode, TextType
from functions import *
import sys
def main():
    base_path = sys.argv[1] if len(sys.argv) > 1 else "/" # Base path for content and public directories
    copy_static_to_public(destination = "docs")
    generate_pages_recursive(dest_dir_path = "docs", dir_path_content = "content", template_path = "template.html", base_path = base_path)


if __name__ == "__main__":
    main()
    