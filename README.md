# RegionStats

[![Tests](https://github.com/biol5472-uofglasgow/GroupA_Project3_RegionStats/actions/workflows/tests.yml/badge.svg)](https://github.com/biol5472-uofglasgow/GroupA_Project3_RegionStats/actions/workflows/tests.yml)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**A command-line tool for computing sequence composition metrics across genomic intervals.**

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
- 📖 **HTML report**: User-friendly output with BedGraph and BigWig support

---

## 🔧 Installation

### Option 1: pip

```bash
pip install git+https://github.com/biol5472-uofglasgow/GroupA_Project3_RegionStats.git
```

*Note: PyPI package will be available in a future release.*

### Option 2: Docker 

```bash
# Build locally
docker build -t regionstats:latest .

# Run with your data
docker run -v $(pwd):/data regionstats:latest \
  --fasta /data/reference.fasta \
  --intervals /data/regions.bed \
  --interval-format bed \
  --output-prefix /data/results \
  --gc-mode include_n
```

### Option 3: From Source

```bash
# Clone the repository
git clone https://github.com/biol5472-uofglasgow/GroupA_Project3_RegionStats.git
cd GroupA_Project3_RegionStats

# Install with uv 
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv
source .venv/bin/activate 
uv pip install .
```

### Requirements

- Python ≥ 3.9
- Dependencies: `pyfaidx`, `pyranges`, `pandas`, `biopython`
- Optional: `pyBigWig` (for BigWig output) , `pyGenomeTracks`
Note: pyBigWig not supported on Windows

### Optional dependencies

```bash
pip install .[pybigwig]
pip install .[pygenometracks]
```
---

## 🚀 Execution

```bash
# Basic usage
regionstats \
  --fasta reference.fasta \
  --intervals regions.bed \
  --interval-format bed \
  --output-prefix results \
  --gc-mode include_n \
  --bedgraph \
  --bigwig \  #optional (Windows not supported)
  --report  
```

**Docker usage:**
```bash
docker run -v $(pwd):/data regionstats:latest \
  --fasta /data/reference.fasta \
  --intervals /data/regions.bed \
  --interval-format bed \
  --output-prefix /data/results \
  --gc-mode include_n
  --bedgraph \
  --bigwig \  #optional (windows not supported)
  --report
```

---

## 📖 Usage

```bash
regionstats --help

usage: Region Stats [-h] --fasta FASTA --intervals INTERVALS --interval-format {bed,gff3} --output-prefix OUTPUT_PREFIX [--gc-mode {include_n,exclude_n}] [--bedgraph] [--bigwig] [--report]

Computes sequence composition metrics for genomic regions.

options:
  -h, --help            show this help message and exit
  --fasta FASTA         Input the path for the Reference genome FASTA file
  --intervals INTERVALS
                        Input the Files for supplying the genomic intervals (BED or GFF3)
  --interval-format {bed,gff3}
                        Input the Format of the intervals file
  --output-prefix OUTPUT_PREFIX
                        Input the Prefix for output files
  --gc-mode {include_n,exclude_n}
                        GC calculation modes: 'include_n' counts the Ns in the denominator; 'exclude_n' ignores the Ns in the denominator
  --bedgraph            Write bedGraph output
  --bigwig              Generate BigWig output (chrom sizes inferred from FASTA)
  --report              Generate an HTML report with summary statistics and plots
```

---

## 📂 Input Files

### Reference FASTA (`ref.fasta`)
- Standard FASTA format

**Example:**
```
>chr1
ATGCATGCNNNATGCATGC
>chr2
GGCCGGCCGGCCGGCC
```

### BED Format (`intervals.bed`)
- Tab-separated: `chrom  start  end  [name]`

**Example:**
```
chr1	0	10	region1
chr1	10	19	region2
chr2	0	16	region3
```

### GFF3 Format (`intervals.gff3`)
- Standard GFF3 

**Example:**
```
chr1	.	region	1	10	.	+	.	ID=region1
chr1	.	region	11	19	.	+	.	ID=region2
```

---

## 📊 Output Files

### `region_metrics.tsv`
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

### `run.json`
JSON metadata file containing:
- Tool version and command
- Input file paths and parameters
- Output file paths
- Summary statistics (number of intervals processed)
- Timestamp

### `region_metrics.bedGraph` (optional)
BedGraph track file for genome browser visualization showing GC content across intervals.

### `region_metrics.bigWig` (optional)
BigWig binary format for efficient genome browser display.

### `report.html`
User-friendly output with summarised metrics plots and track graphs.

### `file.log`
Log file reporting information and error statements.

---

## 🧪 Testing

Run the test suite locally:

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

### Reporting Issues

Found a bug or have a feature request? [Open an issue](https://github.com/biol5472-uofglasgow/GroupA_Project3_RegionStats/issues) on GitHub!

**Please include:**
- RegionStats version (`regionstats --version`)
- Python version
- Operating system
- Error messages and steps to reproduce

---

## 📚 Project Information

### Development Status

**Version:** 1.0.0  
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

---

## 🙏 Acknowledgments

- University of Glasgow BIOL5472 course
- Contributors and maintainers of dependencies: `pyfaidx`, `pyranges`, `pandas`, `biopython`, `pyBigWig`, `pyGenomeTracks`
- The Python bioinformatics community

---
