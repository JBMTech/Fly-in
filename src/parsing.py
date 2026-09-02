from .graph import Graph
from .zone import Zone
from .connection import Connection
from .exceptions import ParsingError
from typing import Dict, Set, Tuple, FrozenSet


class Parser:
    def __init__(self, file_map: str) -> None:
        self.file_map = file_map
        self.nb_drones = 0
        self.zone_names: Set[str] = set()
        self.coordinates: Set[tuple[int, int]] = set()
        self.connections: Set[FrozenSet[str]] = set()
        self.graph = Graph()

    def parsing(self) -> None:
        try:
            with open(self.file_map, "r") as f:
                lines = f.readlines()
        except FileNotFoundError:
            raise ParsingError("Not find File.")
        except PermissionError:
            raise ParsingError("You do not have permission to read this File.")

        if not lines:
            raise ParsingError("The file is empty.")

        nb_drones_exist = False
        start_zone_exist = False
        end_zone_exist = False

        for line_num, line_current in enumerate(lines, start=1):
            try:
                line = line_current.split("#", 1)[0].strip()

                if not line or line.startswith("#"):
                    continue

                lower_line = line.lower()

                if lower_line.startswith("nb_drones:"):
                    if nb_drones_exist:
                        raise ParsingError("nb_drones already exist.")
                    self.valid_nb_drones(line)
                    nb_drones_exist = True

                elif lower_line.startswith("start_hub:"):
                    if start_zone_exist:
                        raise ParsingError("start_hub already exists.")
                    self.valid_zone(line)
                    start_zone_exist = True

                elif lower_line.startswith("hub:"):
                    if not start_zone_exist:
                        raise ParsingError(
                            "start_hub must be defined before hubs.")
                    if end_zone_exist:
                        raise ParsingError(
                            "hub cannot appear after end_hub.")
                    self.valid_zone(line)

                elif lower_line.startswith("end_hub:"):
                    if end_zone_exist:
                        raise ParsingError("end_hub already exists.")
                    self.valid_zone(line)
                    end_zone_exist = True

                elif lower_line.startswith("connection:"):
                    self.valid_connection(line)
                else:
                    raise ParsingError("Invalid Data")

            except ParsingError as ex:
                raise ParsingError(f"line {line_num}: {ex}.")

        if not nb_drones_exist:
            raise ParsingError("nb_drones is missing.")

        if not start_zone_exist:
            raise ParsingError("start_hub is missing.")

        if not end_zone_exist:
            raise ParsingError("end_hub is missing.")


    def valid_nb_drones(self, line: str) -> None:
        aux = line.split(":", 1)

        if len(aux) != 2:
            raise ParsingError("Invalid nb_drones.")
        try:
            nb_drones = int(aux[1].strip())
        except ValueError:
            raise ParsingError("Invalid nb_drones.")
        
        if nb_drones <= 0:
            raise ParsingError("nb_drones must be a positive value.")

        self.nb_drones = nb_drones

    def valid_zone(self, line: str) -> None:

        is_start = False
        is_end = False

        if line.lower().startswith("start_hub:"):
            is_start = line.lower().startswith("start_hub:")
        elif line.lower().startswith("end_hub:"):
            is_end = line.lower().startswith("end_hub:")

        part = line.split(":", 1)
    
        data = part[1].strip()

        metadata: Dict[str, str | int] = {}

        # Obtener información de los metadatos
        if "[" in data and "]" in data:
            if not ("[" in data and data.endswith("]")):
                raise ParsingError("Invalid metadata.")

            data_index = data.find("[")
            metadata_string = data[data_index + 1:-1]

            base_data = data[:data_index].strip()
            metadata = self.valid_metadata(metadata_string)
        else:
            base_data = data

        element = base_data.split()
        if len(element) != 3:
            raise ParsingError(f"<name> <x> <y>, result: {element}")

        name = element[0]
        if name in self.zone_names:
            raise ParsingError(f"Duplicate {name}")
        self.zone_names.add(name)

        X, Y = self.valid_xy(element[1], element[2])
        if (X, Y) in self.coordinates:
            raise ParsingError(f"Duplicate Coordinates ({X}, {Y})") 
        self.coordinates.add((X, Y))

        result_max_drones = int(metadata.get("max_drones", 1))
        zone = str(metadata.get("zone", "normal"))
        color = str(metadata.get("color", "#FFFFFF"))

        new_zone = Zone(name, X, Y, result_max_drones, color, zone)
        self.graph.add_zone(new_zone)

        if is_start:
            self.graph.start_zone = new_zone
        elif is_end:
            self.graph.end_zone = new_zone


    def valid_xy(self, x: str, y: str) -> Tuple[int, int]:
        try:
            X = int(x)
            Y = int(y)
        except ValueError:
            raise ParsingError("Invalid Coordinates")
        return X, Y


    def valid_metadata(self, metadata: str) -> Dict[str, str | int]:
        metadata_result: Dict[str, str | int] = {}
        zone_allowed = ["normal", "restricted", "priority", "blocked"]

        elements = metadata.split()

        for element in elements:

            if element.count("=") != 1:
                raise ParsingError("Invalid metadata.")
            key, value = element.split("=")

            if key in metadata_result:
                raise ParsingError(f"Duplicate metadata: {key}")

            if key == "color":
                if not value:
                    raise ParsingError("Color cannot be empty.")
                metadata_result[key] = value
            elif key == "max_drones":
                try:
                    drones = int(value)
                    if drones <= 0:
                        raise ParsingError("invalud metadata: max_drone")
                    metadata_result[key] = drones
                except ValueError:
                    raise ParsingError("invalid metadato: max_drone")
            elif key == "zone":
                if value in zone_allowed:
                    metadata_result[key] = value
                else:
                    raise ParsingError("invalid metadata: zone not allowed")
            else:
                raise ParsingError(f"Invalid metadata key: {key}")

        return metadata_result


    def valid_connection(self, line: str) -> None:
        elements = line.split(":")

        if len(elements) != 2:
            raise ParsingError("Invalid connection data")  

        data_capacity = 1
        elements[1].strip()

        if "[" in elements[1] and "]" in elements[1]:
            parts = elements[1].split("[", 1)

            if len(parts) != 2:
                raise ParsingError("Invalid metadata.")

            base_data = parts[0].strip()
            metadata_string = parts[1].replace("]", "")
            data_capacity = self.valid_metadata_connection(metadata_string)
        else:
            base_data = elements[1]

        point_connection = base_data.split("-", 1)

        if len(point_connection) != 2:
            raise ParsingError("Invalid connection format.")

        zone1 = point_connection[0].strip()
        zone2 = point_connection[1].strip()

        if not zone1 or not zone2:
            raise ParsingError("Connection contains an empty zone.")

        if zone1 not in self.zone_names:
            raise ParsingError(f"Zone '{zone1}' does not exist.")

        if zone2 not in self.zone_names:
            raise ParsingError(f"Zone '{zone2}' does not exist.")

        if zone1 == zone2:
            raise ParsingError("A zone cannot connect to itself.")

        connection = frozenset([zone1, zone2])

        if connection in self.connections:
            raise ParsingError("Duplicate connection.")

        self.connections.add(connection)
    
        data_connect = Connection(zone1, zone2, data_capacity)
        self.graph.add_connection(data_connect)


    def valid_metadata_connection(self, metadata: str) -> int:

        if not metadata:
            raise ParsingError("Metadata connection is empty.")
    
        key, value = metadata.split("=", 1)

        if key == "max_link_capacity":
            try:
                max_capacity = int(value)
                if max_capacity < 1:
                    raise ParsingError("Metada conection invalid, it must be positive.")
            except ValueError:
                raise ParsingError("Metadata conection invalid.")
        else:
            raise ParsingError("Invalid metadata key.")

        return max_capacity
