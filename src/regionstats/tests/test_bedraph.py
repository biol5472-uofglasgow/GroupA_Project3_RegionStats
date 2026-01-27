import tempfile
from pathlib import Path

from regionstats.bedgraph_bigwig_output import write_bedgraph


def test_bedgraph_written():
    data = [
        {"seqid":"chr1","start":0,"end":10,"gc_fraction":0.5}]

    out = tempfile.NamedTemporaryFile(delete=False)
    out.close()

    write_bedgraph(data, out.name)

    text = Path(out.name).read_text()
    assert "chr1" in text
    assert "0.5000" in text

    Path(out.name).unlink()
