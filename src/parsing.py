from graph import Grahp
from exceptions import ParsingError
from typing import Dict, Set, Tuple, Any


class Parser:
    def __init__(self, file_map: str) -> None:
        self.file_map = file_map
        self.nb_drones = 0
        self.zone_names: Set[str] = set()
        self.cood: Set[tuple[int, int]] = set()
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

        data_index = data.find("[")
        metadata = data[data_index + 1:-1]

        base_data = data[:data_index]
        metadata_string = metadata

        element = base_data.split(" ")
        if len(element) != 3:
            raise ParsingError(f"[ERROR]: <name> <x> <y>, result: {element}")

        name = element[0]
        if name in self.zone_names:
            raise ParsingError(f"[ERROR]: Duplicate {name}")
        self.zone_names.add(name)

        X, Y = self.valid_xy(element[1], element[2])
        if (X, Y) in self.cood:
            raise ParsingError(f"[ERRROR]: Duplicate Coordinates ({X}, {Y})") 
        self.cood.add((X, Y))


    def valid_xy(self, x: str, y: str) -> Tuple[int, int]:
        try:
            X = int(x)
            Y = int(y)
        except ValueError:
            raise ParsingError("[ERROR]: Invalid Coordinates")
        return X, Y


    def valid_connection(self, line: str) -> None:
        ...

    
