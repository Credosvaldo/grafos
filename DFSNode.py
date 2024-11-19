class DFSNode:
    def __init__(self, discovery_time: int, finishing_time: int, parent: str):
        self.discovery_time = discovery_time
        self.finishing_time = finishing_time
        self.parent = str(parent) if parent else None
        
    def __str__(self) -> str:
        return str((self.discovery_time, self.finishing_time, self.parent))
    
    def __repr__(self) -> str:
        return self.__str__()