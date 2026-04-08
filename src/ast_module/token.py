class Token:
    def __init__(self, children=None, start=0, end=0) -> None:
        self.children = children
        self.start = start  # Index in string where token beings
        self.end = end  # Index in string where token ends

    def __repr__(self) -> str:
        raise NotImplementedError
