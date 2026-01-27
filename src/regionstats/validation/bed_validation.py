from .file_validation import validate_file_readable, ValidationError


def validate_bed(path):
    validate_file_readable(path, "BED")

    with open(path) as f:
        line = f.readline().strip()

    if not line:
        raise ValidationError("BED file is empty")

    fields = line.split()
    if len(fields) < 3:
        raise ValidationError("BED must contain at least 3 columns")
