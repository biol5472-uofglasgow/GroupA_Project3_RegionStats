import tempfile
from pathlib import Path
import pytest

from regionstats.validation import (validate_file_path,validate_fasta,validate_bed,validate_gff3,ValidationError)

# creates a small temporary file
def create_temp_file(content="test"):
    f = tempfile.NamedTemporaryFile(delete=False)
    f.write(content.encode())
    f.close()
    return f.name


def test_file_exists():
    path = create_temp_file("abc")
    validate_file_path(path, "test")
    Path(path).unlink()


def test_missing_file():
    with pytest.raises(ValidationError):
        validate_file_path("missing.txt", "test")

#fasta
def test_valid_fasta():
    fasta = create_temp_file(">chr1\nATGC\n")
    validate_fasta(fasta)
    Path(fasta).unlink()

#bed
def test_valid_bed():
    bed = create_temp_file("chr1\t0\t10\n")
    validate_bed(bed)
    Path(bed).unlink()

#gff3
def test_valid_gff3():
    gff = create_temp_file("##gff-version 3\nchr1\tsrc\tregion\t1\t10\t.\t+\t.\tID=x\n")
    validate_gff3(gff)
    Path(gff).unlink()
