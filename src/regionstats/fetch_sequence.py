from pyfaidx import Fasta


def open_fasta(fasta_file str) -> Fasta:
    """
    Open FASTA file for random access using pyfaidx module
    :param fasta_file: FASTA file with sequences
    """
    return Fasta(fasta_file, as_raw=True, sequence_always_upper=True)


def fetch_sequence(fasta_var: Fasta, seqid: str, start: int, end: int) -> str:
    """
    Function to extract sequence data from a FASTA file with specified coordinates

    :param fasta_var: FASTA file variable - fasta_var=open_fasta(fasta_file)
    :param seqid: sequence ID
    :param start: start position of region
    :param end: end position of region
    """
    # Add conditions to catch errors
    if start < 0:
        raise IndexError("Start coordinate cannot be negative")

    if start > end:
        raise ValueError("Start coordinate must be smaller than end coordinate")

    seq_len = len(fasta_var[seqid])
    if end > seq_len:
        raise IndexError("End coordinate exceeds read length")

    return fasta_var[seqid][start:end]
