from pathlib import Path

class ValidationError(Exception):
    pass


def validate_file_readable(path: str, description: str):
    """
    Attempt to open file to ensure it is readable.
    Avoids separate existence checks.
    """
    try:
        with open(path, "r") as f:
            f.readline()
    except FileNotFoundError:
        raise ValidationError(f"{description} file not found: {path}")
    except PermissionError:
        raise ValidationError(f"{description} file not readable: {path}")
