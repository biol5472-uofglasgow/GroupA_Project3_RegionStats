import pytest
from regionstats.bedgraph_bigwig_output import bedgraph_to_bigwig

def test_bigwig_without_pybigwig():
    with pytest.raises(ImportError):
        bedgraph_to_bigwig("a.bg", "b.chrom", "out.bw")
