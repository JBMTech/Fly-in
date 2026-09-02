from .zone import Zone
from .connection import Connection
from typing import List, Dict


class Graph:
    def __init__(self) -> None:
        self.start_zone: Zone | None= None
        self.end_zone: Zone | None = None
        self.zones: Dict[str, Zone] = {}
        self.connections: List[Connection] = []
        self.adjacency_list: Dict[Zone, List[Zone]] = {}

    def add_zone(self, zone: Zone) -> None:
        self.zones[zone.name] = zone
        self.adjacency_list[zone] = []

    def add_connection(self, connection: Connection) -> None:
        self.connections.append(connection)

        zone1 = self.zones[connection.zone1]
        zone2 = self.zones[connection.zone2]

        self.adjacency_list[zone1].append(zone2)
        self.adjacency_list[zone2].append(zone1)
        
        