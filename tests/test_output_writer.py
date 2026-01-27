import pytest
import json
import csv
from pathlib import Path
from regionstats.output_writer import write_tsv, write_run_json

class TestOutputWriter

@pytest.fixture

def generate_mock_records(self):
        # Provides a list of mock result for TSV testing
        return [
            {
                "seqid": "chr1", "start": 10, "end": 20, 
                "name_or_id": "reg1", "length": 10, 
                "gc_fraction": 0.5, "n_fraction": 0.0
            },
            {
                "seqid": "chr2", "start": 100, "end": 200, 
                "name_or_id": "reg2", "length": 100, 
                "gc_fraction": 0.456789123, "n_fraction": 0.1
            }
        ]
def test_write_tsv_success(self, tmp_path, mock_records):
        #Verifies whether TSV is written correctly with headers and formatting

        output_file = tmp_path / "test_output.tsv"
        write_tsv(mock_records, str(output_file))
        content = output_file.read_text().splitlines()

        #Checks the header of the file 
        assert content[0] == "seqid\tstart\tend\tname_or_id\tlength\tgc_fraction\tn_fraction"
        #Checks the row formatting 
        second_row = content[2].split("\t") 
        assert second_row[5] == "0.456789" #checks the decimal formatting 
        #We might need some more tests!


def test_write_run_json_structure(self, tmp_path):
    #Verifies if the JSON metadata contains all required keys and resolved path
       
        json_out = tmp_path / "run_info.json"
        fasta = "dummy.fa"
    #creates a mock json dataset
        write_run_json(
            fasta_path=fasta,
            intervals="test.bed",
            interval_format="bed",
            gc_mode="include_n",
            output_prefix="sample1",
            num_intervals=50,
            output_path=str(json_out)
        )
    #Opens the mock json file and iterates through it 
        with open(json_out, "r") as f:
            data = json.load(f)
        
        assert data["tool"] == "regionstats"
        assert data["summary"]["num_intervals"] == 50
        assert Path(data["inputs"]["fasta"]).is_absolute()
        assert data["inputs"]["interval_format"] == "bed" 
        assert data["inputs"]["fasta"].endswith("dummy.fa")  
        assert data["outputs"]["output_tsv"].startswith("sample1") #checks the output prefix 
        assert "timestamp" in data #checks the presence of the timestamp 
        assert len(data["timestamp"]) > 10 #checks a valid DD MM YYYY