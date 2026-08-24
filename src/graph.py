from zone import Zone
from connection import Connection
from typing import List, Tuple, List, Dict, Any


class Graph:
    def __init__(self) -> None:
        self.start_zone = None
        self.end_zone = None
        self.zones: Dict[str, Any] = {}
        self.connections: List[Connection] = []
        self.route: Dict[List[Any]] = {}

    def add_zone(self, zone: Zone) -> None:
        self.zones[zone.name] = zone
        self.route[zone] = []

    def add_connection(self, connection: Connection) -> None:
        self.connections.append(connection)
        
        