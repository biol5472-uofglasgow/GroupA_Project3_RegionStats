def get_seq_record(fasta_file):
    """
    This function parses through a FASTA file to yield sequence identifiers and data 
    
    :param fasta_file: Input FASTA file containing DNA sequences
    """
    #Opens input FASTA file
    with open(fasta_file) as infile:
        for line in infile:

            #Header lines start with '>'
            if line.startswith('>'):
                #Extract sequence ID (remove '>' and \n)
                id = line.rstrip().lstrip('>')
                #Extract sequence 
                seq = next(infile).rstrip()
            
            #Returns ID and sequence for each record
            yield id, seq   
for record in get_seq_record('ref.fasta'):
    print(record)

