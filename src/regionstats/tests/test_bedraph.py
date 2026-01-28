import tempfile
from pathlib import Path

from regionstats.bedgraph_bigwig_output import write_bedgraph


def test_write_bedgraph_creates_file():
    metrics = [
        {"seqid": "chr1", "start": 0, "end": 10, "gc_fraction": 0.5}
    ]

    out = tempfile.NamedTemporaryFile(delete=False)
    out.close()

    write_bedgraph(metrics, out.name)

    text = Path(out.name).read_text()

    assert "chr1" in text
    assert "0.5000" in text
