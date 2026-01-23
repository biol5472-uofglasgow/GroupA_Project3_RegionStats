
from typing import List, Dict, Any

HEADERS: List[str] = [
    "seqid",
    "start",
    "end",
    "name_or_id",
    "length",
    "gc_fraction",
    "n_fraction",
] #Gives a prior definition of the headers to be used in the tsv file 

"""
    Writes the per-region sequence metrics to a TSV file.
    The output schema has been provided previously hence fixed and defined by HEADERS.

"""

def ouput_tsv(
    records: List[Dict[str, Any]],
    output_path: str
) -> None:
 
    if not records:
        raise ValueError("No records are available for TSV output") #handles empty records 

    with open(output_path, "w", newline="") as out:
       
        out.write("\t".join(HEADERS) + "\n")  # Writes the header line 

        
        for record in records: # Write out the rows in the .tsv file 
            row = [
                str(record["seqid"]),
                str(record["start"]),
                str(record["end"]),
                str(record["name_or_id"]),
                str(record["length"]),
                f"{record['gc_fraction']:.6f}",
                f"{record['n_fraction']:.6f}",
            ]
            out.write("\t".join(row) + "\n") 

import json
from datetime import datetime, timezone
from pathlib import Path

"""
    Write the run metadata to a JSON file.
"""

def write_json(
    fasta_path: str,
    intervals: str,
    interval_format: str,
    gc_mode: str,
    output_prefix: str,
    num_intervals: int,
    output_path: str
) -> None: 
   
    metadata = {
        "tool": "regionstats",
        "version": "0.1.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "inputs": {
            "fasta": str(Path(fasta_path).resolve()),
            "intervals": str(Path(intervals).resolve()),
            "interval_format": interval_format,
        },
        "parameters": {
            "gc_mode": gc_mode,
        },
        "outputs": {
            "output_tsv": f"{output_prefix}_output_tsv.tsv",
            "run_json": f"{output_prefix}_run.json",
            "bedgraph": f"{output_prefix}_region_metrics.bedGraph",
        },
        "summary": {
            "num_intervals": num_intervals,
        },
    }
    
    with open(output_path, "w") as out:
        json.dump(metadata, out, indent=2)
