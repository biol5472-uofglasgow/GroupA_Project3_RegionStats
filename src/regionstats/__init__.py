"""RegionStats package."""

__version__ = "0.1.0"

from .fetch_sequence import open_fasta, fetch_sequence
from .region_metrics import sequence_length, n_fraction, gc_fraction
from .interval_handler import load_intervals
from .bedgraph_bigwig_output import write_bedgraph, bedgraph_to_bigwig
from .validation import ValidationError, validate_file_path, validate_fasta, validate_bed, validate_gff3
