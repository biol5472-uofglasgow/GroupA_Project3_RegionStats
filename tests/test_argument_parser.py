import argparse
import pytest

#For the purpose of testing we decided to split the function into two parts 

def create_parser():
    
#Returns only the configured ArgumentParser object

    parser = argparse.ArgumentParser(prog="Region Stats", description="...") #initialises the argument parser with informations for testing 
    parser.add_argument("--fasta", required=True)
    parser.add_argument("--intervals", required=True)
    parser.add_argument("--interval-format", required=True, choices=["bed", "gff3"])
    parser.add_argument("--output-prefix", required=True)
    parser.add_argument("--gc-mode", choices=["include_n", "exclude_n"], default="include_n")
    parser.add_argument("--bedgraph", action="store_true")
    parser.add_argument("--bigwig", action="store_true")
    return parser

def build_parser(args_list=None):

#Creates the parser and handles the logical validation
    parser = create_parser()
    args = parser.parse_args(args_list) # args_list allows us to insert test strings

    if args.bigwig and not args.bedgraph:
        parser.error("--bigwig requires --bedgraph")
    return args



from regionstats.argument_parser import build_parser

class TestRegionStatsParser:

#Generates a common group of tests for checking the command line interface 

    def base_args(self):
        #Returns a set of mock data 
        return [
            "--fasta", "ref.fasta",
            "--intervals", "test.bed",
            "--interval-format", "bed",
            "--output-prefix", "out"
        ]

    def test_basic_parsing(self, base_args):
        
        args = build_parser(base_args)
        
        assert args.fasta == "ref.fasta"
        assert args.intervals == "test.bed"     
        assert args.interval_format == "bed"    
        assert args.output_prefix == "out"
        assert args.gc_mode == "include_n" #tests for the default values 
        assert args.bigwig is False #also tests for the default values 

    def test_exclude_gc_mode(self, base_args): #Tests for exclusion of n in GC calculation 
        
        base_args.extend(["--gc-mode", "exclude_n"])
        args = build_parser(base_args)

        assert args.gc_mode == "exclude_n"

    #Generates a mock scene where bigwig is provided but BED graph is absent and check if it raises an error 
    def test_bigwig_failure(self, base_args):
        base_args.append("--bigwig")

        with pytest.raises(SystemExit):
            build_parser(base_args)

    #Generates a mock scene where both bigwig and BEDgraph is provided 
    def test_bigwig_success(self, base_args):
      
        base_args.extend(["--bigwig", "--bedgraph"])
        args = build_parser(base_args)
        assert args.bigwig is True
        assert args.bedgraph is True