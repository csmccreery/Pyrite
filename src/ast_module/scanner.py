from .parent_token import ParentToken
from .literal_token import LiteralToken
import re

class Scanner:
    def __init__(self, text):
        self.text = text or ""
        self.trigger_chars = [
                    '*', '-', '_', '#', '`'
                    '>', '&', '[', ']', '(',
                    ')'
                ]
        self.rules = {
                    'header': re.compile(r'^(#+)\s'),
                    'code_block': re.compile(r'^`{3}\n')
                }

    def peek(self, cursor):
        if cursor + 1 < len(self.text):
            return self.text[cursor + 1]
        return None

    def at_start_of_line(self, cursor):
        # Short circuit logic. If the cursor is at the start of the text, we're good
        # If the cursor isn't at the start of the text but the last character was a newline
        # and the current character isn't just another newline. we're good

        return cursor == 0 or (
                    cursor - 1 >= 0 and 
                    (self.text[cursor - 1] == '\n' and self.text[cursor] != '\n')
                )

    def tokenize(self):

        # All the stuff happens here
        block_children = self.block_parse()
        for block in block_children:
            content_start, content_end = block.start, block.end
            if block.token_type == 'header':
                content_start = content_start + block.level + 1
            block.children = self.inline_parse(content_start, content_end)
        return block_children

    def block_parse(self):
        tokens = []
        cursor = 0
        while cursor < len(self.text):
            saved_pos = cursor

            # If the following triggers both the cursor and the saved position *should* be the same
            if self.text[cursor] in self.trigger_chars:
                new_token, current_pos = self.block_dispatcher(saved_pos)
                if new_token:
                    tokens.append(new_token)
                    cursor = current_pos
            else:
                new_token, current_pos = self.paragraph_handler(saved_pos)
                if new_token:
                    tokens.append(new_token)
                    cursor = current_pos

            # Skip empty lines
            while cursor < len(self.text) and self.text[cursor] == '\n':
                cursor += 1 # Still O(n) because both while loops have the same bound and move the same pointer

        return tokens

    def block_dispatcher(self, saved_pos):
        # Check for header level
        header_match = re.match(self.rules['header'], self.text[saved_pos:])
        if header_match: # Newline -> header pattern match
            if self.at_start_of_line(saved_pos):
                header_count = len(header_match[1])
                return self.header_handler(saved_pos, header_count)

        code_block_match = re.match(self.rules['code_block'], self.text[saved_pos:])
        if code_block_match: # Newline -> code block pattern
            if self.at_start_of_line(saved_pos):
                return self.code_block_handler(saved_pos)

        # Just add more regexes to catch more rules

        return self.paragraph_handler(saved_pos)
    
    def header_handler(self, saved_pos, header_count):
        """
            Headers are arguably the easists to implement as they'll never
            go across multiple lines
        """
        cursor = saved_pos
        while cursor < len(self.text) and self.text[cursor] != '\n':
            cursor += 1

        new_block = ParentToken(
                    token_type="header",
                    children=[],
                    start=saved_pos,
                    end=cursor,
                    level=header_count
                )

        return new_block, cursor

    def code_block_handler(self, saved_pos):
        cursor = saved_pos
        # This time all we care about is advancing whole lines until we see the next ```
        while cursor < len(self.text) and self.text[cursor] != '\n':
            if all([char == '`' for char in self.text[cursor + 1:cursor + 3]]):
                # Hit the end of the block
                new_token = ParentToken(
                            token_type="code_block",
                            children=[],
                            start=saved_pos,
                            end=cursor
                        )
                cursor += 3 # Skip past the code ticks
                return new_token
            cursor += 1 # Advance to the next line

    def paragraph_handler(self, saved_pos):
        # While we haven't reached an end of line, and there is another line past that
        # Keep moving the cursor
        cursor = saved_pos
        start_pos = cursor
        while cursor < len(self.text):
            if self.text[cursor] == '\n':
                next_char = self.peek(cursor) # If it's none, we reached the end 
                if not next_char or next_char == '\n': # Two new lines in a row. break

                    new_block = ParentToken(
                                token_type="paragraph",
                                children=[],
                                start=saved_pos,
                                end=cursor,
                            )

                    return new_block, cursor
            cursor += 1
        return None, start_pos

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

        while search_ptr < limit:
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
        while search_ptr < limit:
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
        content_start = cursor + 1
        search_ptr = content_start

        while search_ptr < limit - 1:
            if self.text[search_ptr] == '`':
                content_end = search_ptr

                inner_children = self.inline_parse(content_start, content_end)

                new_token = ParentToken(
                            token_type='code',
                            children=inner_children,
                            start = content_start - 1,
                            end = search_ptr + 1
                        )

