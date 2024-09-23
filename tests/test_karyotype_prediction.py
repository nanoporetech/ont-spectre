import os
import pytest
import urllib.request
import tarfile
import gzip
import shutil

from spectre.main import run_main

# Constants for URLs and file paths
EPI2ME_ARTIFACT_URL = os.environ.get("EPI2ME_ARTIFACT_URL", "default_url")
TEST_DATA_URL = f"{EPI2ME_ARTIFACT_URL}/data/ont-spectre/karyotype_prediction_test_data_v1.tar.gz"
REFERENCE_GENOME_URL = f"{EPI2ME_ARTIFACT_URL}/data/ref/GCA_000001405.15_GRCh38_no_alt_analysis_set.fna.bgzf.gz"

def download_file(url, dest):
    """Download a file from a URL to a destination."""
    with urllib.request.urlopen(url) as response, open(dest, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)

def extract_tar_file(tar_path, extract_path):
    """Extract a tar.gz file."""
    with tarfile.open(tar_path, "r:") as tar:
        tar.extractall(path=extract_path)

def decompress_gzip_file(gz_path, out_path):
    """Decompress a .gz file."""
    with gzip.open(gz_path, 'rb') as f_in, open(out_path, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

@pytest.fixture(scope="session")
def setup_test_environment(tmp_path_factory):
    # Create a temporary directory for the test data
    test_dir = tmp_path_factory.mktemp("karyotype_test_data")
    os.chdir(test_dir)

    # Download and extract test data
    test_data_tar = "karyotype_prediction_test_data_v1.tar.gz"
    download_file(TEST_DATA_URL, test_data_tar)
    extract_tar_file(test_data_tar, test_dir)

    # Download and extract the human hg38 reference genome
    reference_genome_gz = "GCA_000001405.15_GRCh38_no_alt_analysis_set.fna.bgzf.gz"
    download_file(REFERENCE_GENOME_URL, reference_genome_gz)
    
    yield test_dir  # Provide the directory path to the test

    # Cleanup after tests are done
    os.chdir(tmp_path_factory.getbasetemp())  # Change to a safe directory before cleanup
    shutil.rmtree(test_dir)

@pytest.mark.parametrize("sample_dir", ['GM18501', 'GM18861', 'GM18864', 'NA18310'])
def test_karyotype_prediction(setup_test_environment, sample_dir):
    sample_dir_path = setup_test_environment / "karyotype_prediction_test_data" / sample_dir

    # Change the working directory to the sample directory
    os.chdir(sample_dir_path)
    
    args = [
        "CNVCaller",
        "--bin-size", "1000",
        "--coverage", "mosdepth/",
        "--snv", "wf_snp.vcf.gz",
        "--sample-id", "sample",
        "--output-dir", "output_spectre",
        "--reference", "../../GCA_000001405.15_GRCh38_no_alt_analysis_set.fna.bgzf.gz",
        "--metadata", "grch38_metadata",
        "--blacklist", "grch38_blacklist_0.3"
    ]
    # Call the main function which should use the mocked arguments and exit with 0
    with pytest.raises(SystemExit) as exc_info:
        run_main(args)

    assert exc_info.type == SystemExit
    assert exc_info.value.code == 0

    # Read the predicted and expected karyotypes
    with open("output_spectre/predicted_karyotype.txt") as f:
        predicted_karyotype = f.read().strip()

    with open("expected_karyotype.txt") as f:
        expected_karyotype = f.read().strip()

    # Assert that the predicted karyotype matches the expected karyotype
    assert predicted_karyotype == expected_karyotype, f"Karyotype mismatch: {predicted_karyotype} != {expected_karyotype}"
