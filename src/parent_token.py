from .lex_token import Token

class ParentToken(Token):
    def __init__(self, token_type, children, start, end, level=None) -> None:
        super().__init__(token_type, children, start, end)
        self.level = level or -1 # For headings and nesting
        self.children = children or []

    def __repr__(self) -> str:
        return f"ParentToken(Type={self.token_type}, children={[str(child) for child in self.children]}, Start_Index={self.start}, End_Index={self.end}, Level={self.level if self.level else None})"

