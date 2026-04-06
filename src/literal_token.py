from .lex_token import Token

class LiteralToken(Token):
    def __init__(self, start, end) -> None:
        super().__init__(None, None, start, end)

    def __repr__(self) -> str:
        return f"LiteralToken(Start={self.start}, End={self.end})"
