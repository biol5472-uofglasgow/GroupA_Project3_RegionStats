from pyfaidx import Fasta


def write_chrom_sizes_from_fasta(fasta_path, output_path):
    """
    Generate chromosome sizes file from FASTA file path.
    """

    fasta = Fasta(fasta_path)

    with open(output_path, "w") as out:
        for chrom in fasta.keys():
            size = len(fasta[chrom])
            out.write(f"{chrom}\t{size}\n")
