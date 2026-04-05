from pathlib import Path
from lex_token import Token

class AST:
    def __init__(self, md_file_path: str, ast_root: Token):
        self.f_path = Path(md_file_path)
        self.ast_root = ast_root
