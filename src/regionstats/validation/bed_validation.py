from .file_validation import ValidationError, validate_file_path

def validate_bed(bed_path: str):
    """
    Basic BED validation.
    Checks that coordinates are valid and readable.
    """
    validate_file_path(bed_path, "BED")

    with open(bed_path) as bed_file:
        for line_number, line in enumerate(bed_file, start=1):
            line = line.strip()

            # skip empty lines and comments
            if not line or line.startswith("#"):
                continue

            parts = line.split("\t")

            if len(parts) < 3:
                raise ValidationError(
                    f"BED line {line_number} has fewer than 3 columns"
                )

            try:
                start = int(parts[1])
                end = int(parts[2])
            except ValueError:
                raise ValidationError(
                    f"BED line {line_number} has non-integer coordinates"
                )

            if start < 0:
                raise ValidationError(
                    f"BED line {line_number} has negative start coordinate"
                )

            if end <= start:
                raise ValidationError(
                    f"BED line {line_number} has end <= start"
                )
