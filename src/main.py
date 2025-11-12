from textnode import TextNode, TextType
from functions import *

def main():
    text1 = TextNode("Hello, World!", TextType.ITALIC, None)

    print(text1)
    copy_static_to_public()


if __name__ == "__main__":
    main()
    