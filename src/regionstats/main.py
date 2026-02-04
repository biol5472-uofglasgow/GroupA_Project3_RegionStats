"""
Main pipeline for computing region statistics.
v1.0.0
still needs print statements and better error handling
"""

import logging
from pathlib import Path
from typing import Any, Dict, List

from .argument_parser import build_parser
from .bedgraph_bigwig_output import bedgraph_to_bigwig, write_bedgraph
from .chrom_sizes import write_chrom_sizes_from_fasta
from .fetch_sequence import fetch_sequence, open_fasta
from .interval_handler import load_intervals
from .logger import setup_logger
from .output_writer import write_run_json, write_tsv
from .region_metrics import gc_fraction, n_fraction, sequence_length
from .report import generate_report
from .validation import validate_bed, validate_fasta, validate_gff3


def main() -> int:
    """
    Main entry point for region statistics pipeline.

    Returns:
        Exit code (0 for success, non-zero for errors)
    """
    args = build_parser()

    # Create output directory
    output_dir = Path("output_dir")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Log file goes into output_dir
    log_path = output_dir / getattr(args, "log", "regionstats.log")
    setup_logger(log_path)

    logging.info("RegionStats v1.0.0 started")

    # Validate inputs
    try:
        logging.info("Validating FASTA")
        validate_fasta(args.fasta)

        logging.info("Validating interval file")
        if args.interval_format == "bed":
            validate_bed(args.intervals)
        elif args.interval_format == "gff3":
            validate_gff3(args.intervals)

    except Exception:
        logging.exception("Input validation failed")
        return 1

    # Load FASTA and intervals
    try:
        logging.info("Opening FASTA")
        fasta = open_fasta(args.fasta)
        logging.info("Loading intervals")
        intervals = load_intervals(args.intervals, args.interval_format)

    except Exception:
        logging.exception("Failed loading inputs")
        return 1

    # Compute metrics
    metrics: List[Dict[str, Any]] = []

    try:
        logging.info("Computing region metrics")
        for row in intervals.df.itertuples():
            seqid = row.Chromosome
            start = int(row.Start)
            end = int(row.End)

            if hasattr(row, "Name") and row.Name:
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
        logging.info(f"Computed metrics for {len(metrics)} intervals")

    except KeyError as e:
        logging.error(f"Sequence not found: {e}")
        return 1
    except Exception:
        logging.exception("Metric computation failed")
        return 1

    # Write outputs
    try:
        prefix = Path(args.output_prefix).name

        tsv_path = output_dir / f"{prefix}_region_metrics.tsv"
        json_path = output_dir / f"{prefix}_run.json"
        bedgraph_path = output_dir / f"{prefix}_region_metrics.bedGraph"

        logging.info(f"Writing TSV: {tsv_path}")
        write_tsv(metrics, tsv_path)

        if args.bedgraph:
            logging.info(f"Writing bedGraph: {bedgraph_path}")
            write_bedgraph(metrics, bedgraph_path)

        if args.bigwig:
            chrom_sizes_path = output_dir / f"{prefix}.chrom.sizes"
            logging.info("Generating chrom sizes")
            write_chrom_sizes_from_fasta(args.fasta, chrom_sizes_path)

            bigwig_path = output_dir / f"{prefix}_region_metrics.bigwig"
            logging.info("Converting bedGraph to bigwig")
            bedgraph_to_bigwig(bedgraph_path, chrom_sizes_path, bigwig_path)

        logging.info(f"Writing run metadata JSON: {json_path}")
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

    except Exception:
        logging.exception("Failed writing outputs")
        return 1


    # Generate HTML report if requested in CLI
    try:
        if args.report:
            logging.info("Generating HTML report")
            generate_report(
                metrics_tsv=tsv_path,
                run_json=json_path,
                bedgraph_path=bedgraph_path if args.bedgraph else None,
                bigwig_path=bigwig_path if args.bigwig else None,
                chrom_sizes_path=chrom_sizes_path if args.bigwig else None,
                output_dir=output_dir,
            )
            logging.info("HTML report generated in report directory")

    except Exception:
        logging.exception("Report generation failed")
        return 1

    logging.info("RegionStats finished successfully")
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())
