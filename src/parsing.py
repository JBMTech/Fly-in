from graph import Grahp
from zone import Zone
from exceptions import ParsingError
from typing import Dict, Set, Tuple, Any


class Parser:
    def __init__(self, file_map: str) -> None:
        self.file_map = file_map
        self.nb_drones = 0
        self.zone_names: Set[str] = set()
        self.coordinates: Set[tuple[int, int]] = set()
        self.connections: Set[set[str]] = set()
        self.graph = Grahp()

    def parsing(self) -> None:
        try:
            with open(self.file_map, "r") as f:
                lines = f.readlines()
        except FileNotFoundError:
            raise ParsingError("[ERROR]: Not find File.")
        except PermissionError:
            raise ParsingError("[ERROR]: You do not have permission to read this File.")

        if not lines:
            raise ParsingError("[ERROR]: The file is empty.")

        for line_num, line_current in enumerate(lines, start=1):
            try:
                line = line_current.split("#", 1)[0].strip()

                if not line or line.startswith("#"):
                    continue

                lower_line = line.lower()

                if lower_line.startswith("nb_drones"):
                    self.valid_nb_drones(line)

                elif lower_line.startswith("start_hub:"):
                    self.valid_zone(line)

                elif lower_line.startswith("hub:"):
                    self.valid_zone(line)

                elif lower_line.startswith("end_hub:"):
                    self.valid_zone(line)

                elif lower_line.startswith("connection:"):
                    self.valid_connection(line)
                else:
                    raise ParsingError("[ERROR]: Invalid Data")
            except ParsingError as ex:
                raise ParsingError(f"[ERROR]: line {line_num}: {ex}.")


    def valid_nb_drones(self, line: str) -> None:
        aux = line.split(":")

        if len(aux) != 2:
            raise ParsingError("[ERROR]: Invalid nb_drones.")
        try:
            nb_drones = int(aux[1].strip())
        except ValueError:
            raise ParsingError("[ERROR]: Invalid nb_drones.")
        
        if nb_drones <= 0:
            raise ParsingError("[ERROR]: nb_drones must be a positive value.")

        self.nb_drones = nb_drones

    def valid_zone(self, line: str) -> None:

        part = line.split(":", 1)
    
        data = part[1].strip()

        metadata: Dict[str, str | int] = {}

        # Obtener información de los metadatos
        if data in "[" and data in "]":
            data_index = data.find("[")
            metadata_string = data[data_index + 1:-1]

            base_data = data[:data_index]
            metadata = self.valid_metadata(metadata_string)
        else:
            base_data = data

        element = base_data.split(" ")
        if len(element) != 3:
            raise ParsingError(f"[ERROR]: <name> <x> <y>, result: {element}")

        name = element[0]
        if name in self.zone_names:
            raise ParsingError(f"[ERROR]: Duplicate {name}")
        self.zone_names.add(name)

        X, Y = self.valid_xy(element[1], element[2])
        if (X, Y) in self.coordinates:
            raise ParsingError(f"[ERRROR]: Duplicate Coordinates ({X}, {Y})") 
        self.coordinates.add((X, Y))

        result_max_drones = int(metadata.get("max_drones", 1))
        zone = str(metadata.get("zone", "normal"))
        color = str(metadata.get("color", "#FFFFFF"))

        new_zone = Zone(name, X, Y, result_max_drones, color, zone)


    def valid_xy(self, x: str, y: str) -> Tuple[int, int]:
        try:
            X = int(x)
            Y = int(y)
        except ValueError:
            raise ParsingError("[ERROR]: Invalid Coordinates")
        return X, Y


    def valid_metadata(self, metadata: str) -> Dict[str, str | int]:
        metadata_result: Dict[str, str | int] = {}
        zone_allowed = ["normal", "restricted", "priority", "blocked"]

        if metadata.startswith("[") and metadata.endswith("]"):
            elements = metadata.split(" ")

            for element in elements:
                key, value = element.split("=")

                if key == "color":
                    metadata_result[key] = value
                elif key == "max_drones":
                    try:
                        drones = int(value)
                        if drones <= 0:
                            raise ParsingError("[ERROR]: invalud metadata: max_drone")
                        metadata_result[key] = drones
                    except ValueError:
                        raise ParsingError("[ERROR]: invalid metadato: max_drone")
                elif key == "zone":
                    if value in zone_allowed:
                        metadata_result[key] = value
                    else:
                        raise ParsingError("[ERROR]: invalid metadata: zone not allowed")

        return metadata_result


    def valid_connection(self, line: str) -> None:
        elements = line.split(":")

        if len(elements) != 2:
            raise ParsingError("[ERROR]: Invalid connection data")  

        if elements in "[" and elements in "]":
            parts = elements[1].split(" ")
            base_data = parts[0].strip()
            metadata_string = parts[1].replace("[]", "")
            new_data


    def valid_metadata_connection(self, metadata: str) -> Dict[str, int]:

        if not metadata:
            raise ParsingError("[ERROR]: Metadata connection is empty")
        key, value = metadata.split("=")