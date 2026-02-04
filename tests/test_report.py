import json
from pathlib import Path
import os
import subprocess
import pandas as pd
import pytest
from jinja2 import Environment, FileSystemLoader
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from regionstats.report import generate_gc_histogram, generate_n_fraction_histogram, generate_bedgraph_chrom_plots, generate_bigwig_tracks, generate_report

#Create test fixtures for metrics dataframe and file paths
@pytest.fixture
def metrics_df():
    return pd.DataFrame(
        {
            "gc_fraction": [0.4, 0.5, 0.6, 0.45],
            "n_fraction": [0.0, 0.1, 0.0, 0.05],
            "chrom": ["chr1", "chr1", "chr2", "chr2"],
        }
    )

@pytest.fixture
def metrics_tsv(tmp_path, metrics_df):
    path = tmp_path / "metrics.tsv"
    metrics_df.to_csv(path, sep="\t", index=False)
    return path

@pytest.fixture
def run_json(tmp_path):
    data = {
        "inputs": {
            "fasta": "test.fa",
            "intervals": "test.bed",
        },
        "parameters": {"gc_mode": "exclude_n"},
        "summary": {"num_intervals": 4},
        "version": "1.0.0",
        "timestamp": "2025-01-01T12:00:00+00:00",
    }
    path = tmp_path / "run.json"
    path.write_text(json.dumps(data))
    return path


# Test histogram generation functions: file naming and existence
def test_generate_gc_histogram(tmp_path, metrics_df):
    outdir = tmp_path / "out"
    filename = generate_gc_histogram(metrics_df, outdir)

    assert filename == "gc_fraction.png"
    assert (outdir / filename).exists()


def test_generate_n_fraction_histogram(tmp_path, metrics_df):
    outdir = tmp_path / "out"
    filename = generate_n_fraction_histogram(metrics_df, outdir)

    assert filename == "n_fraction.png"
    assert (outdir / filename).exists()


# Test BedGraph chromosome plot generation
def test_generate_bedgraph_chrom_plots(tmp_path):
    bedgraph = tmp_path / "gc.bedGraph"
    bedgraph.write_text(
        "track type=bedGraph\n"
        "chr1\t0\t100\t0.4\n"
        "chr1\t100\t200\t0.5\n"
        "chr2\t0\t100\t0.6\n"
        "chr2\t100\t200\t0.45\n"
        "chr3\t0\t100\t0.55\n"
        "chr4\t300\t400\t0.65\n"
    )

    outdir = tmp_path / "out"
    plots = generate_bedgraph_chrom_plots(bedgraph, outdir)

    assert set(plots.keys()) == {"chr1", "chr2", "chr3", "chr4"} # Check all chromosomes plotted
    for fname in plots.values():
        assert (outdir / fname).exists() # Check all files created


# Test BigWig chromosome plot generation with monkeypatching
def test_generate_bigwig_tracks(monkeypatch, tmp_path):
    # Prepare dummy BigWig and chrom sizes files
    bigwig = tmp_path / "test.bigWig"
    chrom_sizes = tmp_path / "test.chrom.sizes"

    bigwig.write_text("")  # placeholder
    chrom_sizes.write_text(
        "chr1\t1000\nchr2\t2000\nchr3\t1500\nchrx\t500\n"
    )

    outdir = tmp_path / "out"

    # Substitute all subprocess.run calls
    calls = []
    def fake_run(cmd, check):
        calls.append(cmd)
        
    # Patch subprocess.run so no external binary is called
    monkeypatch.setattr(subprocess, "run", fake_run)

    # Run the function
    plots = generate_bigwig_tracks(bigwig, chrom_sizes, outdir)

    # Check all chromosomes are present
    expected_chroms = {"chr1", "chr2", "chr3", "chrx"}
    assert set(plots.keys()) == expected_chroms

    # Ensure output filenames are correct
    for filename in plots.values():
        assert filename.endswith(".png")

    # Ensure subprocess.run was called once per chromosome
    assert len(calls) == len(expected_chroms)



# Test full report generation 
def test_generate_report(
    tmp_path, metrics_tsv, run_json
):
    #Create dummy bedgraph file
    bedgraph = tmp_path / "test.bedGraph"
    bedgraph.write_text(
        "track type=bedGraph\n"
        "chr1\t0\t100\t0.4\n"
        "chr1\t100\t200\t0.5\n"
        "chr2\t0\t100\t0.6\n"
        "chr2\t100\t200\t0.45\n"
        "chr3\t0\t100\t0.55\n"
        "chr4\t300\t400\t0.65\n"
    )

    #Create template directory and file
    template_dir = tmp_path / "src/regionstats"
    template_dir.mkdir(parents=True)

    #Test template file
    template = template_dir / "report_template.html"
    template.write_text(
        "<html>"
        "<body>"
        "<h1>GC report</h1>"
        "{{ provenance.version }}"
        "</body>"
        "</html>"
    )

    cwd = Path.cwd()
    try:
        os.chdir(tmp_path)

        generate_report(
            metrics_tsv=metrics_tsv,
            run_json=run_json,
            bedgraph_path=bedgraph,
        )
    finally:
        os.chdir(cwd)

    report_dir = tmp_path / "report"

    #Test that expected files are created
    assert (report_dir / "report.html").exists()
    assert (report_dir / "gc_fraction.png").exists()
    assert (report_dir / "n_fraction.png").exists()
    assert (report_dir/"gc_fraction_chr1.png").exists()
    assert (report_dir / "run.json").exists()
    assert (report_dir / "test.bedGraph").exists()

    #Check contents of report.html
    html = (report_dir / "report.html").read_text()
    assert "GC report" in html
    assert "1.0.0" in html



