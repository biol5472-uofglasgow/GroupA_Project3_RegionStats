from .file_validation import validate_file_readable
from Bio import SeqIO
from .file_validation import ValidationError


def validate_fasta(path):
    validate_file_readable(path, "FASTA")

    try:
        records = list(SeqIO.parse(path, "fasta"))
    except Exception:
        raise ValidationError("Invalid FASTA format")

    if len(records) == 0:
        raise ValidationError("FASTA contains no sequences")
