class Node:
    def __init__(self, index: int, weight: float = 1):
        self.index = index
        self.weight = weight

    def _str_(self) -> str:
        return str(self.index)

    def __repr__(self) -> str:
        return self._str_()