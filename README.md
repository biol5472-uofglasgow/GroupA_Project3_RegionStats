# RegionStats

[![Tests](https://github.com/biol5472-uofglasgow/GroupA_Project3_RegionStats/actions/workflows/tests.yml/badge.svg)](https://github.com/biol5472-uofglasgow/GroupA_Project3_RegionStats/actions/workflows/tests.yml)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**A fast command-line tool for computing sequence composition metrics across genomic intervals.**
**This a placeholder README and requires edit and review.**

RegionStats extracts sequences from specified genomic regions and calculates statistics like GC content, N-fraction, and sequence length. Designed for bioinformatics workflows requiring quality control and compositional analysis of genomic intervals.

---

## ✨ Features

- 🧬 **Multiple input formats**: BED and GFF3 interval files
- 📊 **Comprehensive metrics**: GC content, N-fraction, sequence length
- ⚙️ **Flexible GC calculation**: Include or exclude ambiguous bases (Ns)
- 🚀 **Fast execution**: Built with uv for rapid dependency resolution
- 📦 **Multiple installation options**: pip, Docker, or from source
- 🐳 **Docker support**: Reproducible containerized execution
- 📈 **Track outputs**: Generate bedGraph files for genome browsers
- 📝 **Metadata logging**: JSON run information for reproducibility

---

## 🔧 Installation

### Option 1: pip (Not Yet Implemented)

```bash
pip install regionstats
```

### Option 2: Docker (Not Yet Implemented)

```bash
# Pull the image
docker pull ghcr.io/biol5472-uofglasgow/regionstats:latest

# Or build locally
docker build -t regionstats:latest .
```

### Option 3: From Source

```bash
# Clone the repository
git clone https://github.com/biol5472-uofglasgow/GroupA_Project3_RegionStats.git
cd GroupA_Project3_RegionStats

# Install with uv (fast)
curl -LsSf https://astral.sh/uv/install.sh | sh
uv pip install -e ".[dev]"

# Or with pip
pip install -e ".[dev]"
```

### Requirements

- Python ≥ 3.9
- Dependencies: `pyfaidx`, `pyranges`, `pandas`, `biopython`, `pyBigWig`

---

## 🚀 Quick Start

```bash
# Basic usage
regionstats \
  --fasta reference.fasta \
  --intervals regions.bed \
  --interval-format bed \
  --output-prefix results \
  --gc-mode include_n
```

**Docker usage:**
```bash
docker run -v $(pwd):/data regionstats:latest \
  --fasta /data/reference.fasta \
  --intervals /data/regions.bed \
  --interval-format bed \
  --output-prefix /data/results \
  --gc-mode include_n
```

---

## 📖 Usage

```bash
regionstats --help
```

### Required Arguments

| Argument | Description |
|----------|-------------|
| `--fasta FASTA` | Path to reference genome FASTA file (indexed with `.fai`) |
| `--intervals INTERVALS` | Path to genomic intervals file (BED or GFF3) |
| `--interval-format {bed,gff3}` | Format of the intervals file |
| `--output-prefix PREFIX` | Prefix for output files |

### Optional Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `--gc-mode {include_n,exclude_n}` | `include_n` | GC calculation mode:<br>• `include_n`: GC / total length<br>• `exclude_n`: GC / (total length - N count) |
| `--bedgraph` | `False` | Generate bedGraph output for genome browsers |
| `--bigwig` | `False` | Generate BigWig output (**requires --bedgraph**) |

---

## 📂 Input Files

### Reference FASTA (`ref.fasta`)
- Standard FASTA format with sequence IDs and bases
- Must be indexed: run `samtools faidx ref.fasta` to generate `ref.fasta.fai`
- Can contain ambiguous bases (Ns)

**Example:**
```
>chr1
ATGCATGCNNNATGCATGC
>chr2
GGCCGGCCGGCCGGCC
```

### BED Format (`intervals.bed`)
- **0-based, half-open coordinates** `[start, end)`
- Tab-separated: `chrom  start  end  [name]`

**Example:**
```
chr1	0	10	region1
chr1	10	19	region2
chr2	0	16	region3
```

### GFF3 Format (`intervals.gff3`)
- **1-based, closed coordinates** `[start, end]` (automatically converted internally)
- Processes only features with `type=region`
- Standard GFF3 columns

**Example:**
```
##gff-version 3
chr1	.	region	1	10	.	+	.	ID=region1
chr1	.	region	11	19	.	+	.	ID=region2
```

---

## 📊 Output Files

### `{prefix}_region_metrics.tsv`
Tab-separated file with one row per interval:

| Column | Description |
|--------|-------------|
| `seqid` | Chromosome/contig name |
| `start` | Start position (0-based) |
| `end` | End position (0-based, exclusive) |
| `name_or_id` | Region name or auto-generated ID |
| `length` | Sequence length in bases |
| `gc_fraction` | GC content (0.0 - 1.0) |
| `n_fraction` | Fraction of ambiguous bases (0.0 - 1.0) |

**Example:**
```
seqid	start	end	name_or_id	length	gc_fraction	n_fraction
chr1	0	10	region1	10	0.500000	0.000000
chr1	10	19	region2	9	0.444444	0.333333
```

### `{prefix}_run.json`
JSON metadata file containing:
- Tool version and command
- Input file paths and parameters
- Output file paths
- Summary statistics (number of intervals processed)
- Timestamp

### `{prefix}_region_metrics.bedGraph` (optional)
bedGraph track file for genome browser visualization showing GC content across intervals.

### `{prefix}_region_metrics.bigWig` (optional)
BigWig binary format for efficient genome browser display.


### `HTML` (Under Development)


---

## 💡 Examples

### Example 1: Basic Analysis

```bash
regionstats \
  --fasta genome.fasta \
  --intervals coding_regions.bed \
  --interval-format bed \
  --output-prefix output/coding \
  --gc-mode include_n
```

**Output:**
- `output/coding_region_metrics.tsv`
- `output/coding_run.json`

---

### Example 2: Exclude Ns from GC Calculation

```bash
regionstats \
  --fasta draft_genome.fasta \
  --intervals assembly_gaps.bed \
  --interval-format bed \
  --output-prefix gaps_analysis \
  --gc-mode exclude_n
```


---

### Example 3: Generate Genome Browser Tracks

```bash
regionstats \
  --fasta reference.fasta \
  --intervals enhancers.gff3 \
  --interval-format gff3 \
  --output-prefix enhancer_gc \
  --gc-mode include_n \
  --bedgraph \
  --bigwig
```

**Output:**
- TSV and JSON files
- `enhancer_gc_region_metrics.bedGraph`
- `enhancer_gc_region_metrics.bigWig` (for UCSC/IGV)

---

### Example 4: Docker with Volume Mounting

```bash
# All files in current directory
docker run -v $(pwd):/data regionstats:latest \
  --fasta /data/ref.fasta \
  --intervals /data/regions.bed \
  --interval-format bed \
  --output-prefix /data/results \
  --gc-mode include_n
```

---

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest tests/ -v

# Run specific test module
pytest tests/test_region_metrics.py -v

# Run with coverage report
pytest tests/ --cov=regionstats --cov-report=html
```

**CI/CD Status:** Tests automatically run on every push via GitHub Actions across Ubuntu, macOS, and Windows with Python 3.9-3.12.

---

### Development Status

**Version:** 0.1.0  
**Status:** Active Development

This tool was developed as part of BIOL5472 at the University of Glasgow. While functional and tested, it is under active development. Feedback and contributions are welcome!

### Authors

- Mohammad Alsuwaidi
- Sasha Chew  
- Faizul Hasan Qazi
- Lohith Venkatachala

**Institution:** University of Glasgow

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### MIT License Summary

- ✅ **Commercial use** allowed
- ✅ **Modification** allowed
- ✅ **Distribution** allowed
- ✅ **Private use** allowed
- ⚠️ **Liability** and **warranty** not provided

---

## 🙏 Acknowledgments

- University of Glasgow BIOL5472 course
- Contributors and maintainers of dependencies: `pyfaidx`, `pyranges`, `pandas`, `biopython`, `pyBigWig`
- The Python bioinformatics community
