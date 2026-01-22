def write_bedgraph(interval_metrics, output_path):
    """
    Write GC fraction per interval as a bedGraph file.
    """
    if not interval_metrics:
        return

    with open(output_path, "w") as out:
        out.write('track type=bedGraph name="GC_fraction"\n')

        for region in interval_metrics:
            try:
                chrom = region["seqid"]
                start = int(region["start"])
                end = int(region["end"])
                gc = float(region["gc_fraction"])
            except (KeyError, ValueError, TypeError):
                raise ValueError("Invalid interval data for bedGraph output")

            out.write(f"{chrom}\t{start}\t{end}\t{gc:.4f}\n")
