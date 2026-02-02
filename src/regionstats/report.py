import json
import subprocess
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from jinja2 import Environment, FileSystemLoader
from matplotlib.ticker import MaxNLocator


def generate_gc_histogram(df, outdir):
    """
    Generate and save a histogram plot of GC fraction 
    distribution across all regions and chromosomes
    """
    outdir.mkdir(exist_ok=True)

    # Change bin number according to number of intervals
    if len(df) <= 50:
        bins = 10
    elif len(df) <= 200:
        bins = 20
    else:
        bins = 30

    plt.figure(figsize=(6, 4))
    plt.hist(
        df["gc_fraction"], bins=bins, color="skyblue", edgecolor="black", alpha=0.85
    )

    plt.xlabel("GC fraction", fontsize=11, fontweight="bold")
    plt.ylabel("Number of regions", fontsize=11, fontweight="bold")
    plt.title("GC fraction distribution", fontsize=12, fontweight="bold", pad=8)

    # Y-grid and integer ticks
    plt.grid(axis="y", linestyle="--", alpha=0.4)
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.tight_layout()

    # Save plot
    hist_path = outdir / "gc_fraction.png"
    plt.savefig(hist_path, dpi=300)
    plt.close()
    return hist_path.name


def generate_n_fraction_histogram(df, outdir):
    """
    Generate a histogram of N fraction per interval.
    """
    if len(df) <= 50:
        bins = 10
    elif len(df) <= 200:
        bins = 20
    else:
        bins = 30

    plt.figure(figsize=(6, 4))

    plt.hist(df["n_fraction"], bins=bins, color="salmon", edgecolor="black", alpha=0.85)

    plt.xlabel("N fraction", fontsize=11, fontweight="bold")
    plt.ylabel("Number of regions", fontsize=11, fontweight="bold")
    plt.title("N fraction distribution", fontsize=12, fontweight="bold", pad=8)

    # Y-grid and integer ticks
    plt.grid(axis="y", linestyle="--", alpha=0.4)
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.tight_layout()

    # Save plot
    hist_path = outdir / "n_fraction.png"
    plt.savefig(hist_path, dpi=300)
    plt.close()

    return hist_path.name


def generate_bedgraph_chrom_plots(bedgraph_path, outdir):
    """
    Generate per-chromosome GC fraction bar plots from a 
    BedGraph if --bigwig not provided
    """
    # Check if BedGraph file exists
    bedgraph_path = Path(bedgraph_path)
    if not bedgraph_path.exists():
        return {}

    # Ensure output directory exists
    outdir.mkdir(exist_ok=True)

    # Read BedGraph file
    df_bg = pd.read_csv(
        bedgraph_path,
        sep="\t",
        header=None,
        names=["chrom", "start", "end", "value"],
        skiprows=1,
    )
    chroms = df_bg["chrom"].unique()

    # Create dict to store chromosome plot files
    chrom_plots = {}

    for chrom in chroms:
        chr_df = df_bg[df_bg["chrom"] == chrom]

        # Prepare data for plotting
        x = (chr_df["start"] + chr_df["end"]) / 2  # Midpoint for bar
        y = chr_df["value"]
        widths = chr_df["end"] - chr_df["start"]  # Width of each bar

        # Create bar plot
        plt.figure(figsize=(10, 3))
        plt.bar(x, y, width=widths, color="steelblue", align="center", linewidth=0)
        plt.ylim(0, 1)
        plt.xlabel("Genomic position (bp)", fontsize=11, fontweight="bold")
        plt.ylabel("GC fraction", fontsize=11, fontweight="bold")
        plt.title(f"GC fraction along {chrom}", fontsize=12, pad=8, fontweight="bold")

        plt.grid(axis="y", linestyle="--", alpha=0.4)
        plt.tight_layout()

        # Save plot into output directory "report"
        plot_file = outdir / f"gc_fraction_{chrom}.png"
        plt.savefig(plot_file, dpi=300)
        plt.close()

        # Store plot file name into dict
        chrom_plots[chrom] = plot_file.name

    return chrom_plots


def generate_bigwig_tracks(bigwig_path, chrom_sizes_path, outdir):
    """
    Generate per-chromosome GC fraction plots using pyGenomeTracks from 
    a BigWig file if both --bigwig and --bedgraph provided
    """
    # Check if BigWig and chrom sizes files exist
    bigwig_path = Path(bigwig_path)
    chrom_sizes_path = Path(chrom_sizes_path)

    if not bigwig_path.exists() or not chrom_sizes_path.exists():
        return {}

    chrom_sizes = pd.read_csv(
        chrom_sizes_path, sep="\t", header=None, names=["chrom", "length"]
    )

    # Ensure output directory exists
    outdir.mkdir(exist_ok=True)

    chrom_plots = {}  # Create dict to store chromosome plot files

    # Iterate through chromosomes to create plots
    for _, row in chrom_sizes.iterrows():
        chrom = row["chrom"]
        start = 0
        end = row["length"]

        # Calculate ideal bin number based on chromosome length
        target_reso = 1000  # target resolution in base pairs
        chrom_length = row["length"]  # in base pairs
        bin_size = max(1, chrom_length // target_reso)  # ensure bin size is at least 1
        number_of_bins = chrom_length // bin_size

        # Create pyGenomeTracks config file
        config_file = outdir / f"{chrom}_track.ini"
        with open(config_file, "w") as f:
            f.write("[GC fraction]\n")
            f.write(f"file = {bigwig_path}\n")
            f.write("file_type = bigwig\n")
            f.write("title = GC fraction\n")
            f.write("color = #0d6607\n")
            f.write("alpha=1\n")
            f.write("min_value = 0\n")
            f.write("max_value = 1\n")
            f.write("height = 8\n")
            f.write(f"number_of_bins={number_of_bins}\n")

        # Create output plot file for each chromosome
        output_file = outdir / f"gc_fraction_{chrom}.png"

        # Call pyGenomeTracks CLI to generate plot
        subprocess.run(
            [
                "pyGenomeTracks",
                "--tracks",
                str(config_file),
                "--region",
                f"{chrom}:{start}-{end}",
                "--outFileName",
                str(output_file),
                "--dpi",
                "300",
            ],
            check=True,
        )

        chrom_plots[chrom] = output_file.name

    return chrom_plots


def generate_report(
    metrics_tsv, run_json, bedgraph_path=None, bigwig_path=None, chrom_sizes_path=None
):
    """
    Generate HTML report summarising generated outputs and metrics. Includes:
    - Provenance information from json file
    - GC fraction histogram
    - Per-chromosome GC fraction plots if --bedgraph or --bigwig provided

    Also produces:
    - Copies of run.json and bedGraph into report directory
    - PNG files for plots
    - Config files for pyGenomeTracks if --bigwig provided

    """
    # Convert paths to Path objects
    metrics_tsv = Path(metrics_tsv)
    run_json = Path(run_json)
    report_dir = Path("report")  # Output "report" directory
    report_dir.mkdir(exist_ok=True)

    # Read metrics TSV and run json files
    df = pd.read_csv(metrics_tsv, sep="\t")
    json_data = json.loads(run_json.read_text())

    # Generate GC and N fraction histogram
    gc_plot = generate_gc_histogram(df, report_dir)
    n_plot = generate_n_fraction_histogram(df, report_dir)

    # Determines which track plotting method to use: if BedGraph provided only, 
    #use BedGraph; else if BigWig provided, use BigWig
    if (
        bigwig_path
        and Path(bigwig_path).exists()
        and chrom_sizes_path
        and Path(chrom_sizes_path).exists()
    ):
        # Use pyGenomeTracks CLI for BigWig if exists
        gc_chrom_plots = generate_bigwig_tracks(
            bigwig_path, chrom_sizes_path, report_dir
        )

    elif bedgraph_path and Path(bedgraph_path).exists():
        # Else use Bedgraph matplotlib if --bigwig not provided
        gc_chrom_plots = generate_bedgraph_chrom_plots(bedgraph_path, report_dir)

    else:  # No chromosome plots if neither provided
        gc_chrom_plots = {}

    # Copy provenance + BedGraph
    (report_dir / "run.json").write_text(run_json.read_text())
    if bedgraph_path and Path(bedgraph_path).exists():
        (report_dir / Path(bedgraph_path).name).write_text(
            Path(bedgraph_path).read_text()
        )

    # Render HTML
    env = Environment(loader=FileSystemLoader("src/regionstats"))
    template = env.get_template("report_template.html")
    html = template.render(
        columns=list(df.columns),
        rows=df.to_dict(orient="records"),
        provenance={
            "fasta": json_data["inputs"]["fasta"],
            "intervals": json_data["inputs"]["intervals"],
            "gc_mode": (
                "Include N"
                if json_data["parameters"]["gc_mode"] == "include_n"
                else "Exclude N"
            ),
            "version": json_data["version"],
        },
        bedgraph=Path(bedgraph_path).name if bedgraph_path else None,
        gc_histogram=gc_plot,
        n_histogram=n_plot,
        gc_chrom_plots=gc_chrom_plots,
    )

    (report_dir / "report.html").write_text(html)
    print(f"Report generated at: {report_dir / 'report.html'}")
