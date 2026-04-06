from .token import Token
from enum import Enum

class ParentTokenType(Enum):
    PARAGRAPH = "paragraph"
    HEADER = "header"
    CODE_BLOCK = "code_block"
    U_LIST = "unordered_list"
    O_LIST = "ordered_list"
    BLOCK_QUOTE = "block_quote"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    IMAGE = "image"
    LINK = "link"
    WIKI_LINK = "wiki_link"

class ParentToken(Token):
    def __init__(self, token_type, children, start, end, data) -> None:
        super().__init__(children, start, end)
        self.token_type = token_type
        self.data = data or {} # For URLs, links, images, header levels, etc
        self.children = children or []

    def __repr__(self) -> str:
        return f"ParentToken(Type={self.token_type}, children={[str(child) for child in self.children]}, Start_Index={self.start}, End_Index={self.end}, Data={[(key, self.data[key]) for key in self.data]})"

