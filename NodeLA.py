class NodeLA:
    def __init__(self, weight: float = None, name: str = None):
        self.weight = weight
        self.name = name

    def _str_(self) -> str:
        return str(self.index)

    def __repr__(self) -> str:
        return self._str_()
