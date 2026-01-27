import pytest
from regionstats.bedgraph_bigwig_output import bedgraph_to_bigwig

def test_bigwig_missing_files():
    with pytest.raises(FileNotFoundError):
        bedgraph_to_bigwig("missing.bg", "missing.chrom", "out.bw")
