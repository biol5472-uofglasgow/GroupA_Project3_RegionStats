# Project 3: Computing Interval Sequence Metrics
This tool extracts sequences for specified genomic intervals and computes sequence statistics such as GC fractions and N fractions. Reference sequences are extracted from a reference FASTA file, and genomic intervalsare  stored in BED or GFF3 files.

By: Mohammad Alsuwaidi, Sasha Chew, Faizul Hasan Qazi, Lohith Venkatachala

# Input files
- Reference FASTA file: e.g `ref.fasta`
  — Contains sequences with or without Ns
  - Indexed '.fai' file must be generated for random access
- Interval files:
  - BED file: e.g `intervals.bed` — named intervals across contigs
    - 0-based, half-open intervals
  - GFF3 file: e.g `intervals.gff3` — same regions represented as features
    - 1-based, closed intervals (converted to 0-based, half-open in script)
    - Process only feature type: region
    
# Output files
- region_metrics.tsv: tab-separated file containing one row per interval
  - Columns: seqid, start, end, name_or_id, length, gc_fraction, n_fraction
- run.json: contains run metadata, parameters, outputs, and summary statistics
- region_metrics.bedGraph: interval metrics as a track-like output

# Usage
`usage: Region Stats [-h] --fasta FASTA --intervals INTERVALS --interval-format {bed,gff3} --output-prefix OUTPUT_PREFIX [--gc-mode {include_n,exclude_n}]`

Computes sequence composition metrics for genomic regions.

options:
  
  --fasta FASTA     Input the path for the Reference genome FASTA file
  
  --intervals     INTERVALS Input the Files for supplying the genomic intervals (BED or GFF3)
                        
  --interval-format {bed,gff3}
                        Input the Format of the intervals file
                        
  --output-prefix OUTPUT_PREFIX
                        Input the Prefix for output files
                        
  --gc-mode {include_n,exclude_n}
                        GC calculation modes: 'include_n' counts the Ns in the denominator; 'exclude_n' ignores the Ns in the denominator

# Installation
Requires Python xxx

Dependencies:

Install dependencies:

