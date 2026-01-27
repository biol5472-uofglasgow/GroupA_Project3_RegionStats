import tempfile
from pathlib import Path

from regionstats.chrom_sizes import write_chrom_sizes_from_fasta


def test_chrom_sizes():
    fasta = tempfile.NamedTemporaryFile(delete=False)
    fasta.write(b">chr1\nATGC\n>chr2\nAAAAAA\n")
    fasta.close()

    out = tempfile.NamedTemporaryFile(delete=False)
    out.close()

    write_chrom_sizes_from_fasta(fasta.name, out.name)

    text = Path(out.name).read_text()
    assert "chr1\t4" in text
    assert "chr2\t6" in text

    Path(out.name).unlink()
