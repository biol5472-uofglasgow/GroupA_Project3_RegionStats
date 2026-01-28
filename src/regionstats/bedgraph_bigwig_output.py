from pathlib import Path

try:
    import pyBigWig
except ImportError:
    pyBigWig = None


def write_bedgraph(interval_metrics, output_path):
    """
    Write GC fraction per interval as a bedGraph file.
    """
    if not interval_metrics:
        return

    with open(output_path, "w") as out:
        out.write('track type=bedGraph name="GC_fraction"\n')

        for region in interval_metrics:
            chrom = region["seqid"]
            start = int(region["start"])
            end = int(region["end"])
            gc = float(region["gc_fraction"])

            out.write(f"{chrom}\t{start}\t{end}\t{gc:.4f}\n")


def bedgraph_to_bigwig(bedgraph_path, chrom_sizes_path, bigwig_path):
    """
    Convert a bedGraph file into a BigWig file for genome browser use.
    """

    bedgraph_path = Path(bedgraph_path)
    chrom_sizes_path = Path(chrom_sizes_path)

    if not bedgraph_path.exists():
        raise FileNotFoundError(f"bedGraph not found: {bedgraph_path}")

    if not chrom_sizes_path.exists():
        raise FileNotFoundError(f"Chrom sizes file not found: {chrom_sizes_path}")

    if pyBigWig is None:
        raise ImportError("pyBigWig is required for BigWig output")

    chrom_sizes = []
    with open(chrom_sizes_path) as f:
        for line in f:
            chrom, size = line.strip().split()
            chrom_sizes.append((chrom, int(size)))

    bw = pyBigWig.open(str(bigwig_path), "w")
    bw.addHeader(chrom_sizes)

    with open(bedgraph_path) as bg:
        for line in bg:
            if line.startswith("track") or line.startswith("#"):
                continue

            chrom, start, end, value = line.strip().split()

            bw.addEntries(
               [chrom],
               [int(start)],
                ends=[int(end)],
                values=[float(value)],
            )

    bw.close()
