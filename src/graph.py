from .zone import Zone
from .connection import Connection
from typing import List, Dict, Any


class Graph:

    def __init__(self) -> None:
        """
        Initialize an empty graph with zones, connections,
        and adjacency mappings.
        """
        self.start_zone: Zone | Any = None
        self.end_zone: Zone | Any = None

        self.zones: Dict[str, Zone] = {}

        self.connections: List[Connection] = []

        self.adjacency_list: Dict[Zone, List[Zone]] = {}

        self.connection_maps: Dict[
            tuple[str, str],
            Connection
        ] = {}

    def add_zone(self, zone: Zone) -> None:
        self.zones[zone.name] = zone
        """Add a zone to the graph and initialize its adjacency list."""
        self.adjacency_list[zone] = []

    def add_connection(self, connection: Connection) -> None:
        """
        Add a connection between two zones and
        update the graph's adjacency mappings.
        """

        self.connections.append(connection)

        zone1 = self.zones[connection.zone1]
        zone2 = self.zones[connection.zone2]

        self.adjacency_list[zone1].append(zone2)
        self.adjacency_list[zone2].append(zone1)

        self.connection_maps[
            (zone1.name, zone2.name)
        ] = connection

        self.connection_maps[
            (zone2.name, zone1.name)
        ] = connection

    def get_connection(
        self,
        zone1: str,
        zone2: str
    ) -> Connection | Any:
        """
        Return the connection between two zones,
        or None if no connection exists.
        """

        return self.connection_maps.get(
            (zone1, zone2)
        )
