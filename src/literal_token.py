from lex_token import Token

class LiteralToken(Token):
    def __init__(self, value) -> None:
        super().__init__(value, None, None)
        self.value = value or ""

    def __eq__(self, other) -> bool:
        if not isinstance(other, LiteralToken):
            return False

        return self.value == other.value
