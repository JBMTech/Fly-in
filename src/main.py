import sys
from typing import Any

def valid_arg() -> Any:
    if len(sys.argv) == 3:
        return sys.argv[2]
    else:
        print("Usage: python3 main.py MAP=<map_file>")
        sys.exit(1)

def main() -> None:
    file_map = valid_arg()
    


if __name__ == "__main__":
    main()