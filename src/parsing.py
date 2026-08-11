from graph import Grahp
from typing import Dict, Set, Any


class Parser:
    def __init__(self, file_map: str) -> None:
        self.file_map = file_map
        self.total_drones = 0
        self.zone_names: Set[str] = set()
        self.positions: Set[tuple[int, int]] = set()
        self.seen_connections: Set[set[str]] = set()
        self.graph = Grahp()

    def parsing(self) -> None:
        try:
            with open(self.file_map, "r") as f:
                lines = f.readlines()
        except Exception:
            ...

        if not lines:
            print("[ERROR]: The file is empty")

        for line_num, line_current in enumerate(lines, start=1):
            try:
                line = line_current.split("#", 1)[0].strip()

                if not line or line.startswith("#"):
                    continue

                lower_line = line.lower()