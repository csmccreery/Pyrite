class Token:
    def __init__(self, token_type=None, children=None, start=0, end=0) -> None:
        self.token_type = token_type
        self.children = children
        self.start = start # Index in string where token beings
        self.end = end # Index in string where token ends
    
    def __repr__(self) -> str:
        raise NotImplementedError

    def __eq__(self, other) -> bool:
        raise NotImplementedError

