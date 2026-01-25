from pathlib import Path

def write_chrom_sizes_from_fasta(fasta, output_path):
    """
    Generate chromosome sizes file from an opened FASTA object.
    """
    with open(output_path, "w") as out:
        for chrom in fasta.keys():
            length = len(fasta[chrom])
            out.write(f"{chrom}\t{length}\n")
