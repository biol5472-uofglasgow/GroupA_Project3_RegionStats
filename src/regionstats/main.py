"""
Main pipeline for computing region statistics.
v0.1.0
still needs print statements and better error handling
"""

from pathlib import Path
from typing import List, Dict, Any

from .argument_parser import build_parser
from .fetch_sequence import open_fasta, fetch_sequence
from .interval_handler import load_intervals
from .region_metrics import sequence_length, n_fraction, gc_fraction
from .output_writer import write_tsv, write_run_json
from .validation import validate_fasta, validate_bed, validate_gff3
from .chrom_sizes import write_chrom_sizes_from_fasta
from .bedgraph_bigwig_output import write_bedgraph, bedgraph_to_bigwig

def main() -> int:
    """
    Main entry point for region statistics pipeline.
    
    Returns:
        Exit code (0 for success, non-zero for errors)
    """
    args = build_parser()
    
    print(f"RegionStats v0.1.0")
    
    # Validate inputs
    print(f"Validating inputs...")
    try:
        validate_fasta(args.fasta)
        if args.interval_format == "bed":
            validate_bed(args.intervals)
        elif args.interval_format == "gff3":
            validate_gff3(args.intervals)
        
    except Exception as e:
        return 1
    
    # Load FASTA and intervals
    try:
        fasta = open_fasta(args.fasta)
        intervals = load_intervals(args.intervals, args.interval_format)
        
    except Exception as e:
        return 1
    
    # Compute metrics
    metrics: List[Dict[str, Any]] = []
    
    try:
        for row in intervals.df.itertuples():
            seqid = row.Chromosome
            start = int(row.Start)
            end = int(row.End)
            
            if hasattr(row, 'Name') and row.Name:
                name = row.Name
            else:
                name = f"{seqid}:{start}-{end}"
            
            seq = fetch_sequence(fasta, seqid, start, end)
            
            region_data = {
                "seqid": seqid,
                "start": start,
                "end": end,
                "name_or_id": name,
                "length": sequence_length(seq),
                "gc_fraction": gc_fraction(seq, mode=args.gc_mode),
                "n_fraction": n_fraction(seq),
            }
            metrics.append(region_data)
        
    except KeyError as e:
        print(f"Sequence not found: {e}")
        return 1
    except Exception as e:
        print(f"Computation error: {e}")
        return 1
    
    # Write outputs
    try:
        tsv_path = f"{args.output_prefix}_region_metrics.tsv"
        json_path = f"{args.output_prefix}_run.json"
        bedgraph_path = f"{args.output_prefix}_region_metrics.bedGraph"
        
        output_dir = Path(args.output_prefix).parent
        if output_dir != Path("."):
            output_dir.mkdir(parents=True, exist_ok=True)
        
        write_tsv(metrics, tsv_path)
        write_bedgraph(metrics, bedgraph_path)
        if args.bigwig:
            chrom_sizes_path = f"{args.output_prefix}.chrom.sizes"
            write_chrom_sizes_from_fasta(fasta, chrom_sizes_path)

            bigwig_path = f"{args.output_prefix}_region_metrics.bigWig"
            bedgraph_to_bigwig(
                bedgraph_path,
                chrom_sizes_path,
                bigwig_path)
        write_run_json(
            fasta_path=args.fasta,
            intervals=args.intervals,
            interval_format=args.interval_format,
            gc_mode=args.gc_mode,
            output_prefix=args.output_prefix,
            num_intervals=len(metrics),
            output_path=json_path,
        )
        
        print(f"Completed. Processed {len(metrics)} intervals.")
        
    except Exception as e:
        print(f"Error writing outputs: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
