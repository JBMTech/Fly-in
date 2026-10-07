from .zone import Zone
from .connection import Connection
from typing import List, Dict


class Graph:

    def __init__(self) -> None:
        self.start_zone: Zone | None = None
        self.end_zone: Zone | None = None

        self.zones: Dict[str, Zone] = {}

        self.connections: List[Connection] = []

        self.adjacency_list: Dict[Zone, List[Zone]] = {}

        self.connection_maps: Dict[
            tuple[str, str],
            Connection
        ] = {}

    def add_zone(self, zone: Zone) -> None:
        # Realizamos un diccioanrio de "nombre de zona" -> Zona
        self.zones[zone.name] = zone
        """
        Inicializamos un diccionario que contiene
        como valor una lista de zonas "Zona -> Lista de Zonas"
        """
        self.adjacency_list[zone] = []

    def add_connection(self, connection: Connection) -> None:

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
    ) -> Connection | None:

        return self.connection_maps.get(
            (zone1, zone2)
        )
