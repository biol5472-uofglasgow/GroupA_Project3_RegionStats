import pytest
import pyranges as pr
from interval_handler import load_intervals
from pathlib import Path


# Define paths to test interval files
TEST_DIR = Path(__file__).resolve().parent.parent
BED_PATH = TEST_DIR / "intervals.bed"
GFF_PATH = TEST_DIR / "intervals.gff3"

# Sanity check to ensure test files exist
def test_interval_files_exist():
    assert BED_PATH.exists()
    assert GFF_PATH.exists()


# Test loading BED intervals
def test_load_bed_intervals():
    bed_intervals = load_intervals(str(BED_PATH), format='bed')
    assert isinstance(bed_intervals, pr.PyRanges)
    assert not bed_intervals.df.empty # Ensure DataFrame is not empty
    assert len(bed_intervals) == 5  # Assuming intervals.bed has 5 intervals


#Test BED files have required columns
def test_bed_intervals_columns():
    bed_intervals = load_intervals(str(BED_PATH), format='bed')
    expected_columns = {'Chromosome', 'Start', 'End'}
    assert expected_columns.issubset(set(bed_intervals.columns))


# Test loading GFF3 intervals with 'region' features only
def test_load_gff3_intervals():
    gff_intervals = load_intervals(str(GFF_PATH), format='gff3', featuretype={'region'})
    assert isinstance(gff_intervals, pr.PyRanges)
    assert not gff_intervals.df.empty # Ensure DataFrame is not empty
    assert len(gff_intervals) == 5  # Assuming intervals.gff3 has 5 'region' features


#Test GFF3 files have required columns
def test_gff3_intervals_columns():
    gff_intervals = load_intervals(str(GFF_PATH), format='gff3', featuretype={'region'})
    expected_columns = {'Chromosome', 'Start', 'End'}
    assert expected_columns.issubset(set(gff_intervals.columns))


# Test GFF3 files have dropped unnecessary columns
def test_gff3_intervals_dropped_columns():
    gff_intervals = load_intervals(str(GFF_PATH), format='gff3', featuretype={'region'})
    dropped_columns = {'Source', 'Feature', 'Score', 'Frame'}
    assert dropped_columns.isdisjoint(set(gff_intervals.columns))


# Test that loading intervals with invalid format raises ValueError
def test_load_intervals_invalid_format_bed():
    with pytest.raises(ValueError):
        load_intervals(str(BED_PATH), format='invalid_format')

def test_load_intervals_invalid_format():
    with pytest.raises(ValueError):
        load_intervals('dummy_file.txt', format='txt')


# Test that coordinates are valid for loaded intervals
def test_intervals_coordinates_valid_bed():
    bed_intervals=load_intervals(str(BED_PATH), format='bed')
    df=bed_intervals.df
    assert (df['Start'] >= 0).all()  # Start positions should be non-negative
    assert (df['End'] > df['Start']).all()  # End positions should be greater than Start positions

def test_intervals_coordinates_valid_gff3():
    gff_intervals=load_intervals(str(GFF_PATH), format='gff3', featuretype={'region'})
    df=gff_intervals.df
    assert (df['Start'] >= 0).all()  # Start positions should be non-negative
    assert (df['End'] > df['Start']).all()  # End positions should be greater than Start positions   

