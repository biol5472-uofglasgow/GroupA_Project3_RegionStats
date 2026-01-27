
"""
    This function returns the length of the region isolated from the sequence
"""


def sequence_length(seq: str) -> int:

    seq_length = len(seq)
    return seq_length


# Checks for the proper running of the sequence_length function
assert sequence_length("ATGC") == 4
assert sequence_length("atgc") == 4
assert sequence_length("atg") == 3

"""
    Return the fraction of ambiguous base calls in the region isolated from the sequence

"""


def n_fraction(seq: str) -> float:

    if not seq:  # If empty string is passed on then returns a zero value
        return 0.0

    seq_upper: str = (
        seq.upper()
    )  # standardisation of the sequence by converting every base into a upper case
    n_count: int = seq_upper.count("N")  # counts the number of ambiguous base calls

    n_fraction: float = n_count / len(
        seq_upper
    )  # counts the fraction of N in the isolated region

    return n_fraction


# Checks for the proper running of the n_fraction function
assert n_fraction("ATGC") == 0
assert n_fraction("atgc") == 0
assert n_fraction("ATNN") == 0.5
assert n_fraction("NNNN") == 1
assert n_fraction("ATng") == 0.25
assert n_fraction("nnnn") == 1

"""
    Returns the GC fraction of the isolated region
    *******************
    Parameters involved
    *******************
    seq : str - DNA sequence of a specific region isolated from the genomic FASTA file
    mode : str
    'include_n' -> GC / total length #Includes the (Ambiguous Base Calls(Ns)  in the calculation of the GC content
    'exclude_n' -> GC / (total length - N count) #Excludes the (Ambiguous Base Calls(Ns)  in the calculation of the GC content
"""


def gc_fraction(seq: str, mode: str = "include_n") -> float:

    if not seq:
        return 0.0

    seq_upper: str = seq.upper()

    g_count: int = seq_upper.count("G")  # Counts the number of Gs
    c_count: int = seq_upper.count("C")  # Counts the number of Cs
    n_count: int = seq_upper.count("N")  # Counts the number of Ns

    gc_count: int = g_count + c_count  # Calculates the total number of Gs and Cs
    total_len: int = len(
        seq_upper
    )  # Calculates the length of a given region including the Ns
    gc_fraction: float = 0.0
    # If the mode given is exclude_n then the operations are as follows

    if mode == "exclude_n":

        effective_length: int = (
            total_len - n_count
        )  # Substracts the number of Ns from the total length
        if (
            effective_length == 0
        ):  # If the entire stretch of the sequence comprises of Ns
            return 0.0  # Checks against ZeroDivisionErrors
        gc_fraction = gc_count / effective_length
        return gc_fraction

    # Default: includes the Ns in the calculation of length
    gc_fraction = gc_count / total_len
    return gc_fraction


# Checks for the proper running of the gc_fraction function
assert gc_fraction("ATGC") == 0.5
assert gc_fraction("atgc") == 0.5
assert gc_fraction("GGGG") == 1
assert gc_fraction("CCCC") == 1
assert gc_fraction("NNNN") == 0
assert gc_fraction("ATGCN") == 0.4
