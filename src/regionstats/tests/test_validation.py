import tempfile
import pytest
from pathlib import Path

from regionstats.validation import (
    validate_fasta,
    validate_bed,
    validate_gff3,
)


def test_validate_fasta_valid():
    f = tempfile.NamedTemporaryFile(delete=False)
    f.write(b">chr1\nATGC\n")
    f.close()

    validate_fasta(f.name)

#fasta
def test_validate_fasta_invalid():
    f = tempfile.NamedTemporaryFile(delete=False)
    f.write(b"ATGC\n")
    f.close()

    with pytest.raises(Exception):
        validate_fasta(f.name)

#bed
def test_validate_bed_valid():
    f = tempfile.NamedTemporaryFile(delete=False)
    f.write(b"chr1\t0\t10\n")
    f.close()

    validate_bed(f.name)

#gff3
def test_validate_gff3_valid():
    f = tempfile.NamedTemporaryFile(delete=False)
    f.write(b"##gff-version 3\n")
    f.close()

    validate_gff3(f.name)
