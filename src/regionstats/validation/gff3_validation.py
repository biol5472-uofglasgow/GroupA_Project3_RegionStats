from .file_validation import ValidationError, validate_file_path

def validate_gff3(gff3_path: str):
    """
    Basic GFF3 validation.
    Checks header, column count, and coordinates.
    """
    validate_file_path(gff3_path, "GFF3")

    header_found = False

    with open(gff3_path) as gff_file:
        for line_number, line in enumerate(gff_file, start=1):
            line = line.strip()

            if line.startswith("##gff-version 3"):
                header_found = True
                continue

            if not line or line.startswith("#"):
                continue

            if not header_found:
                raise ValidationError(
                    "GFF3 file is missing '##gff-version 3' header"
                )

            parts = line.split("\t")

            if len(parts) != 9:
                raise ValidationError(
                    f"GFF3 line {line_number} does not have 9 columns"
                )

            try:
                start = int(parts[3])
                end = int(parts[4])
            except ValueError:
                raise ValidationError(
                    f"GFF3 line {line_number} has non-integer coordinates"
                )

            if start < 1:
                raise ValidationError(
                    f"GFF3 line {line_number} has start < 1"
                )

            if end < start:
                raise ValidationError(
                    f"GFF3 line {line_number} has end < start"
                )
