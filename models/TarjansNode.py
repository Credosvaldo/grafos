class TarjansNode:
    def __init__(self, visited: bool, parent: str, disc: int, low: int):
        self.visited = visited
        self.parent = parent
        self.disc = disc
        self.low = low