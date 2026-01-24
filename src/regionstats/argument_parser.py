import argparse


def build_parser() -> argparse.Namespace:
    """
    This function takes in the necessary arguments from the user 
    Using the command line interface 
    """
    parser = argparse.ArgumentParser( prog="Region Stats",description=("Computes sequence composition metrics for genomic regions."))

    # Defines the parser for the FASTA file 
    parser.add_argument( "--fasta",required=True,help="Input the path for the Reference genome FASTA file" )

    # Defines the parser for the BED/GFF file 
    parser.add_argument("--intervals",required=True,help="Input the Files for supplying the genomic intervals (BED or GFF3)")

    # Defines the parser for allowing the user to select thr type of file included in the script
    parser.add_argument("--interval-format",required=True,choices=["bed", "gff"],help="Input the Format of the intervals file")

    #Allows the user to input the prefix for the output files 
    parser.add_argument("--output-prefix",required=True,help="Input the Prefix for output files")

    #Allows the user to choose between two options for the method to calculate the GC content 
    parser.add_argument("--gc-mode",choices=["include_n", "exclude_n"],default="include_n",help=("GC calculation modes: "
            "'include_n' counts the Ns in the denominator; "
            "'exclude_n' ignores the Ns in the denominator"))

    # Enables bedGraph output
    parser.add_argument( "--bedgraph", action="store_true", help="Write bedGraph output")

    # Enables BigWig output
    parser.add_argument( "--bigwig", action="store_true", help="Convert bedGraph to BigWig")

    # Chromosome sizes file (required for BigWig)
    parser.add_argument( "--chrom-sizes", help="Chromosome sizes file (required for BigWig output)")

    return parser.parse_args()

