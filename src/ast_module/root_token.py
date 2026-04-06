from .token import Token

class RootToken(Token):
    def __init__(self, file_path, children=None):
        super().__init__(children or [], -1, -1)
        self.file_path = file_path

    def __repr__(self) -> str:
        str_children = None
        if self.children:
            str_children = [str(child) for child in self.children]
        return f"Root(File Path = {self.file_path}\nTree = {str_children})"
