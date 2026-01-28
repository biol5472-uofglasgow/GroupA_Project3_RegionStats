import pytest
from regionstats.region_metrics import sequence_length, n_fraction, gc_fraction

#Test for the function sequence_length
def test_sequence_length_original():
    seq = "ATGC"
    result = sequence_length(seq)
    assert result == 4

def test_sequence_length_case_insensitivity():
    assert sequence_length("atgc") == 4
    assert sequence_length("aTgC") == 4 

# Tests for the N fraction 

def test_n_fraction_mixed():
    seq = "ATNN"
    result = n_fraction(seq)
    assert result == 0.5

def test_n_fraction_empty():
    assert n_fraction("") == 0.0

def test_n_fraction_ambiguous():
    assert n_fraction("nnnn") == 1.0
    assert n_fraction("NNNN") == 1.0 

def test_n_fraction_case():
    assert n_fraction("ATGC") == 0.0
    assert n_fraction("atgc") == 1.0 

# Test for GC Fraction 

def test_gc_fraction_including_N():
    seq = "ATGCN"
    result = gc_fraction(seq, mode="include_n")
    assert result == 0.4

def test_gc_fraction_excluding_n():
    seq = "ATGCN"
    result = gc_fraction(seq, mode="exclude_n")
    assert result == 0.5

def test_gc_fraction_all_ambiguous_check():
    result = gc_fraction("NNNN", mode="exclude_n")
    assert result == 0.0
