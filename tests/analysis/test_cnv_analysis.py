import pytest
import numpy as np
from unittest.mock import MagicMock, mock_open

from spectre.analysis.analysis import CNVAnalysis

@pytest.fixture
def cnv_analysis():
    coverage_file = "dummy_coverage_file"
    coverage_mosdepth_data = MagicMock()
    coverage_mosdepth_data.genome_mean_coverage = 30

    bin_size = 1000
    output_directory = "dummy_output_directory"
    outbed = "dummy_outbed"
    outvcf = "dummy_outvcf"
    genome_info = {
        "chromosomes": ["chr1", "chrX", "chrY"],
        "chr_lengths_by_name": {"chr1": 1000, "chrX": 1000, "chrY": 1000}
    }
    sample_id = "dummy_sample_id"
    snv_file = "dummy_snv_file"
    metadata_ref = {}
    
    return CNVAnalysis(
        coverage_file, coverage_mosdepth_data, bin_size, output_directory, outbed, outvcf, genome_info, 
        sample_id, metadata_ref, snv_file, only_chr_list="chrX,chrY,chr1", as_dev=True
    )

@pytest.mark.parametrize("normalized_cov, expected_ploidy", [
    (1.3, 1),
    (2.0, 2),
    (2.7, 3),
])
def test_detect_chromosome_ploidy(cnv_analysis, normalized_cov, expected_ploidy):
    cnv_analysis.lower_2n_threshold = 1.5
    cnv_analysis.upper_2n_threshold = 2.5

    ploidy = cnv_analysis.detect_chromosome_ploidy(normalized_cov)
    assert ploidy == expected_ploidy

@pytest.mark.parametrize("chrX_copies, chrY_copies", [
    (1, 0),
    (1, 1),
    (1, 2),
    (2, 0),
    (2, 1),
    (2, 2),
    (3, 0),
    (3, 1),
    (3, 2),
])
def test_chromosome_ploidy_detection_combinations(monkeypatch, cnv_analysis, chrX_copies, chrY_copies):
    chrX_coverage = 30 * chrX_copies / cnv_analysis.ploidy
    chrY_coverage = 30 * chrY_copies / cnv_analysis.ploidy

    read_data = f'chrX\t0\t1000\t{chrX_coverage}\nchrY\t0\t1000\t{chrY_coverage}\n'
    m = mock_open(read_data=read_data)
    monkeypatch.setattr('builtins.open', m)

    cnv_analysis.coverages_df_diploid = MagicMock()
    cnv_analysis.coverages_df_diploid['coverage_'].median.return_value = 30
    cnv_analysis.coverages_df_diploid['coverage_'].quantile.side_effect = [20, 40]

    cnv_analysis.data_normalization()

    assert cnv_analysis.sex_choromosome_ploidies['chrX'] == chrX_copies
    assert cnv_analysis.sex_choromosome_ploidies['chrY'] == chrY_copies
