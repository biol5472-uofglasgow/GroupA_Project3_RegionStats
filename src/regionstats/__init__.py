"""RegionStats package."""

__version__ = "0.1.0"

from .bedgraph_bigwig_output import bedgraph_to_bigwig, write_bedgraph
from .fetch_sequence import fetch_sequence, open_fasta
from .interval_handler import load_intervals
from .region_metrics import gc_fraction, n_fraction, sequence_length
from .validation import (
    ValidationError,
    validate_bed,
    validate_fasta,
    validate_file_path,
    validate_gff3,
)
