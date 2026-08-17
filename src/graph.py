from typing import List, Tuple, List, Dict, Any


class Grahp:
    def __init__(self) -> None:
        self.start_zone = None
        self.end_zone = None
        self.zones: Dict[str, Any] = {}
        self.connections: List[Any] = []
        self.route: Dict[List[Any]] = {}
        