from pyfaidx import Fasta

def open_fasta(fasta_file):
    """
    Open FASTA file for random access using pyfaidx module
    :param fasta_file: FASTA file with sequences
    """
    return Fasta(fasta_file, as_raw=True, sequence_always_upper=True)


def fetch_sequence(fasta_var, seqid, start, end):
    """
    Function to extract sequence data from a FASTA file with specified coordinates
    
    :param fasta_var: FASTA file variable - fasta_var=open_fasta(fasta_file)
    :param seqid: sequence ID
    :param start: start position of region
    :param end: end position of region
    """
    return fasta_var[seqid][start:end]







