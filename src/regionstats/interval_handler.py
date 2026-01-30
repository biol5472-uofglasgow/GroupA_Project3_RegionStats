import pyranges as pr


def load_intervals(interval_file, format, featuretype={"region"}):
    """
    Loads BED or GFF3 intervals using 0-based, half-open notation
    Input: BED/GFF3 file, file format, feature type
    """
    format = format.lower()  # Ensure format is in lowercase
    interval_file=str(interval_file) #Convert Path object to string


    if format == "bed":
        return pr.read_bed(interval_file)  # If file is in .bed format

    elif format == "gff3":
        gen_range = pr.read_gff3(interval_file)

        if featuretype is not None:
            gen_range = gen_range[
                gen_range.Feature.isin(featuretype)
            ]  # Produces rows with only the desired feature type (default: region)

        gen_range = gen_range.drop(
            ["Source", "Feature", "Score", "Frame"]
        )  # Drop unnecessary columns

        return gen_range  # If file is in .gff3 format

    else:  # Raise value error if unsupported format entered
        raise ValueError(f"Invalid format {format}. Enter either gff3 or bed!")
