from pathlib import Path
from typing import Mapping 

def write_chrom_sizes_from_fasta(fasta:Mapping[str,str], output_path:Path)-> None: 
    """
    Generate chromosome sizes file from an opened FASTA object.
    """
    with open(output_path, "w") as out:
        for chrom in fasta.keys():
            length = len(fasta[chrom])
            out.write(f"{chrom}\t{length}\n")
