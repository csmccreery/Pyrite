from .lex_token import Token
from .parent_token import ParentToken
from .literal_token import LiteralToken
import re

class Scanner:
    def __init__(self, text, position=0):
        self.text = text or ""
        self.position = position
        self.trigger_chars = [
                    '*', '-', '_', '#', '`'
                    '>', '&', '[', ']', '(',
                    ')'
                ]
        self.block_rules = {
                    'header': re.compile(r'^(#+)\s'),
                    'code_block': re.compile(r'^`{3}\n')
                }

    def peek(self):
        if self.position + 1 < len(self.text):
            return self.text[self.position + 1]
        return None

    def tokenize(self):
        root = ParentToken("root", None, None, None)

        # All the stuff happens here
        root.children = self.block_parse()
        for block in root.children:
            content_start, content_end = block.start, block.end
            if block.token_type == 'header':
                content_start = content_start + block.level + 1
            block.children = self.inline_parse(content_start, content_end)
        return root

    def block_parse(self):
        tokens = []
        while self.position < len(self.text):
            saved_pos = self.position
            tokens.append(self.block_dispatcher(saved_pos))

            # Skip empty lines
            while self.position < len(self.text) and self.text[self.position] == '\n':
                self.position += 1

        return tokens

    def block_dispatcher(self, saved_pos):
        if re.match(self.block_rules['header'], self.text[saved_pos:]):
            header_count = len(re.match(self.block_rules['header'], self.text[saved_pos:])[1])
            return self.header_handler(saved_pos, header_count)

        if re.match(self.block_rules['code_block'], self.text[saved_pos:]):
            return self.code_block_handler(saved_pos)

        # Just add more regexes to catch more rules

        return self.paragraph_handler(saved_pos)

    
    def header_handler(self, saved_pos, count):
        """
            Headers are arguably the easists to implement as they'll never
            go across multiple lines
        """
        while self.position < len(self.text) and self.text[self.position] != '\n':
            self.position += 1

        new_block = ParentToken(
                    token_type="header",
                    children=[],
                    start=saved_pos,
                    end=self.position,
                    level=count
                )

        return new_block

    def code_block_handler(self, saved_pos):
        # This time all we care about is advancing whole lines until we see the next ```
        while self.position < len(self.text) and self.text[self.position] != '\n':
            if all([char == '`' for char in self.text[self.position + 1:self.position + 3]]):
                # Hit the end of the block
                new_token = ParentToken(
                            token_type="code_block",
                            children=[],
                            start=saved_pos,
                            end=self.position
                        )
                self.position += 3 # Skip past the code ticks
                return new_token
            self.position += 1

    def paragraph_handler(self, saved_pos):
        # While we haven't reached an end of line, and there is another line past that
        # Keep moving the cursor
        while self.position < len(self.text) and self.text[self.position] != '\n':
            next_char = self.peek()
            if next_char or next_char != '\n':
                self.position += 1

        new_block = ParentToken(
                    token_type="paragraph",
                    children=[],
                    start=saved_pos,
                    end=self.position,
                )

        return new_block

    def inline_parse(self, start, end):
        cursor = start
        tokens = []

        last_processed_pos = start

        while cursor < end:
            if self.text[cursor] in self.trigger_chars:
                # If this is actually a token and not someone just randomly 
                # throwing asterisks in their markdown then we do the following
                new_token, next_pos = self.inline_dispatch(cursor, end)
                if new_token:
                    if cursor > last_processed_pos:
                        tokens.append(LiteralToken(last_processed_pos, cursor))

                    tokens.append(new_token)

                    cursor = next_pos
                    last_processed_pos = cursor
                    continue

            cursor += 1
        if last_processed_pos < end:
            tokens.append(LiteralToken(last_processed_pos, end))

        return tokens

    def inline_dispatch(self, cursor, limit):
        if self.text[cursor] == "*":
            if self.text[cursor + 1] == "*":
                return self.handle_inline_bold(cursor + 2, limit)

            return self.handle_inline_italic(cursor, limit)

        if self.text[cursor] == "_":
            return self.handle_inline_italic(cursor, limit)

        if self.text[cursor] == '`':
            return self.handle_inline_code(cursor, limit)

        return None, cursor 

    def handle_inline_bold(self, cursor, limit):
        content_start = cursor + 2
        search_ptr = content_start

        while search_ptr < limit - 1:
            if self.text[search_ptr] == '*' and self.text[search_ptr + 1] == '*':
                content_end = search_ptr

                inner_children = self.inline_parse(content_start, content_end)

                new_token = ParentToken(
                            token_type="bold",
                            children=inner_children,
                            start=content_start - 2,
                            end=search_ptr + 2
                        )

                return new_token, search_ptr + 2

            search_ptr += 1

        return None, cursor

    def handle_inline_italic(self, cursor, limit):
        search_char = self.text[cursor] # Is it a '_' or a '*'?
        content_start = cursor + 1
        search_ptr = content_start
        
        # While our moving pointer is less than the limit
        while search_ptr < limit - 1:
            if self.text[search_ptr] == search_char:
                content_end = search_ptr

                inner_children = self.inline_parse(content_start, content_end)

                new_token = ParentToken(
                            token_type="italic",
                            children=inner_children,
                            start=content_start - 1,
                            end=search_ptr + 1
                        )
                return new_token, search_ptr + 1

            search_ptr += 1

        return None, cursor


    def handle_inline_code(self, cursor, limit):
        pass

