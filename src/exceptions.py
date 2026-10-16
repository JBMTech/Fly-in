
class ParsingError(Exception):
    """Raised when the input file contains invalid data or formatting."""
    ...


class FileError(Exception):
    """Raised when the input file cannot be accessed or read."""
    ...
