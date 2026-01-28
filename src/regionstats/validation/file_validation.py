from pathlib import Path


class ValidationError(Exception):
    """Raised when input validation fails."""

    pass


def validate_file_path(path: str, description: str):
    p = Path(path)

    if not p.exists():
        raise ValidationError(f"{description} file not found: {path}")

    if not p.is_file():
        raise ValidationError(f"{description} is not a file: {path}")

    if p.stat().st_size == 0:
        raise ValidationError(f"{description} file is empty: {path}")
