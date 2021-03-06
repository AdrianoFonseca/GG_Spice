class Component():
    def __init__(self, id, nodes, value):
        self.id = id
        self.value = value
        self.nodes = nodes
        self.type = None
        self.linear = True
        self.dynamic = False

    def __repr__(self) -> str:
        _str = f"Component {self.id} of type {self.type} and value {self.value} between nodes {self.nodes}"
        return _str