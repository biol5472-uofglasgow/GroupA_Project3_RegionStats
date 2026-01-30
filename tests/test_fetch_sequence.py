import pytest
from pyfaidx import Fasta
from fetch_sequence import open_fasta, fetch_sequence


# Fixture to provide a reference FASTA file for pytests
@pytest.fixture(scope="session")
def ref_fasta():
    return open_fasta("ref.fasta")


#Tests that open_fasta function returns a Fasta object
def test_open_fasta_returns_fasta_object(ref_fasta):
    assert isinstance(ref_fasta, Fasta)


#Tests that Fasta object contains expected sequence IDs
def test_open_fasta_contains_chr1(ref_fasta):
    assert "chr1" in ref_fasta

def test_open_fasta_contains_chr2(ref_fasta):
    assert "chr2" in ref_fasta


#Tests that fetch_sequence returns correct subsequences
def test_fetch_sequence_returns_correct_start(ref_fasta):
    seq=fetch_sequence(ref_fasta, "chr1", 0, 10)
    assert seq == "ACGTACGTAC"

def test_fetch_sequence_returns_correct_middle(ref_fasta):
    seq=fetch_sequence(ref_fasta, "chr1", 20,40)
    assert seq=="ACGTACGTACGTNNNNACGT"

def test_fetch_sequence_returns_correct_end(ref_fasta):
    seq=fetch_sequence(ref_fasta, "chr2", 56, 68)
    assert seq == "AAAACCCCGGGG"

def test_fetch_sequence_empty_region(ref_fasta):
    seq=fetch_sequence(ref_fasta, "chr1", 10, 10)
    assert seq == ""

def test_fetch_sequence_single_nucleotide(ref_fasta):
    seq=fetch_sequence(ref_fasta, "chr2", 30, 31)
    assert seq == "G"

def test_fetch_sequence_full_length(ref_fasta):
    seq=fetch_sequence(ref_fasta, "chr1", 0, len(ref_fasta["chr1"]))
    assert seq == "ACGTACGTACGTACGTACGTACGTACGTACGTNNNNACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGT"


#Tests that fetch_sequence raises KeyError for invalid sequence ID
def test_fetch_sequence_invalid_seqid(ref_fasta):
    with pytest.raises(KeyError):
        fetch_sequence(ref_fasta, "chr3", 0, 10)


#Tests that fetch_sequence raises IndexError for out-of-bounds coordinates
def test_fetch_sequence_out_of_bounds_start(ref_fasta):
    with pytest.raises(IndexError):
        fetch_sequence(ref_fasta, "chr1", -5, 10)

def test_fetch_sequence_out_of_bounds_end(ref_fasta):
    with pytest.raises(IndexError):
        fetch_sequence(ref_fasta, "chr2", 0, 1000)


#Tests that fetch_sequence raises ValueError for start greater than end
def test_fetch_sequence_start_greater_than_end(ref_fasta):
    with pytest.raises(ValueError):
        fetch_sequence(ref_fasta, "chr1", 10, 5)





