from Bio import SeqIO

from .file_validation import ValidationError, validate_file_path


def validate_fasta(fasta_path: str):
    validate_file_path(fasta_path, "FASTA")

    records = list(SeqIO.parse(fasta_path, "fasta"))

    if not records:
        raise ValidationError("FASTA file has no sequences")

    for record in records:
        seq = str(record.seq).upper()

        if not seq:
            raise ValidationError(f"Empty sequence in {record.id}")

        for base in seq:
            if base not in "ACGTN":
                raise ValidationError(f"Invalid base '{base}' in {record.id}")
