from .parent_token import ParentToken

class Scanner:
    def __init__(self, text, position=0):
        self.text = text or ""
        self.position = position
        self.special_chars = [
                    '#',
                    '*'
                    ''
                ]

    def tokenize(self):
        root = ParentToken("root", None, None, None)

        # All the stuff happens here
        block_tokens = self.block_parse()
        root.children = block_tokens
        return root

    def block_parse(self):
        tokens = []
        while self.position < len(self.text):
            if self.text[self.position] in 
            saved_pos = self.position
            
            is_header = self.text[self.position] == "#"
            token_type = "header" if is_header else "paragraph"

            self.dispatcher(saved_pos, self.text[self.position])


            # Skip empty lines
            while self.position < len(self.text) and self.text[self.position] == '\n':
                self.position += 1

        return tokens

    def dispatcher(self, saved_pos, current_char):
        match current_char:
            case '#': # Handle headers
                self.handle_header(saved_pos)
            case '> ': # Handle quotes
                pass
            case '-': # Handle lists
                pass
            case '*': # Handle lists, bold, or italic
                pass
            case '`': # Handle code
                pass
            case '_': # Handle italics (alt)
                pass
            case _:
                pass

    def handle_header(self, saved_pos):
        while self.position < len(self.text) and self.text[self.position] != '\n':
            self.position += 1

        new_block = ParentToken(
                    token_type="header",
                    children=[],
                    start=saved_pos,
                    end=self.position,
                )

        return new_block
      




