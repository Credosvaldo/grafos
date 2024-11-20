class Node:
    def __init__(self, index: int, weight: float = None):
        self.index = index
        self.weight = weight

    def _str_(self) -> str:
        return str(self.index)

    def __repr__(self) -> str:
        return self._str_()