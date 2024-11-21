class Edge:
    
    def __init__(self, name: str = None, weight=1) -> None:
        self.name = name
        self.weight = weight
        
    def __str__(self) -> str:
        return str(self.weight)
    
    def __repr__(self) -> str:
        return self.__str__()