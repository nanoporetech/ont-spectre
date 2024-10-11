![Spectre](./logo.png)

# Spectre - Long-read CNV Caller

[Spectre](https://github.com/fritzsedlazeck/Spectre/tree/main) is a long-read copy number variation (CNV) caller designed to detect large CNVs (>100kb).

**Ont-spectre** is a tool based on the original Spectre, with the following main enhancements:
* **Diploid Coverage Estimation:** Bins containing heterozygous SNVs are used to estimate the properties of the diploid coverage distribution, aiding in the selection of appropriate parameters.
* **Karyotype Prediction:** Adds sex chromosome karyotype prediction (including XO, XXY, etc). All events are called relative to the predicted karyotype.

## Installation

The recommended way to install Spectre is through either `pip` or `conda`:

```bash
pip install ont-spectre

```
(or)
```bash
conda install nanoporetech::ont-spectre
```

> **Note**: Spectre supports Python versions >= 3.8.

## Build from Source

To install the `ont-spectre` tool from the source, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/epi2me-labs/ont-spectre.git
   cd ont-spectre
   ```

2. **Create a virtual environment (optional):**

   It’s recommended to use a isolated environment to manage dependencies. Create and activate one with:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

   Alternatively, you can create a conda environment:

   ```bash
   conda create -n spectre python=3.8 pip -y
   conda activate spectre
   ```

> **Note**: Spectre supports Python versions >= 3.8.

3. **Install dependencies and the tool:**

   ```bash
   pip install .
   ```

4. **Verify installation:**

   After installation, you should be able to run the tool using the entry point `spectre`:

   ```bash
   spectre --help
   ```

## How to run

Spectre requires the following inputs:
- The output directory of [mosdepth](https://github.com/brentp/mosdepth), a tool for fast coverage calculation.
- The reference genome (can be bgzip-compressed).
- The window size used in Mosdepth (Ensure that the binsize between Mosdepth and Spectre matches. We suggest a binsize of 1,000 base pairs).
- A VCF file containing SNVs (Single Nucleotide Variants).

### Example Command:

```bash
spectre CNVCaller \
  --bin-size 1000 \
  --coverage mosdepth/sampleid/ \
  --sample-id sampleid \
  --output-dir sampleid_output_directory_path/ \
  --reference reference.fasta.gz \
  --snv sampleid.vcf.gz
```

## Help

**Licence and Copyright**

© 2024- Oxford Nanopore Technologies Ltd.

`ont-spectre` is distributed under the terms of the Oxford Nanopore Technologies Public License v1.0.

**Research Release**

Research releases are provided as technology demonstrators to provide early
access to features or stimulate Community development of tools. Support for
this software will be minimal and is only provided directly by the developers.
Feature requests, improvements, and discussions are welcome and can be
implemented by forking and pull requests. However much as we would
like to rectify every issue and piece of feedback users may have, the
developers may have limited resource for support of this software. Research
releases may be unstable and subject to rapid iteration by Oxford Nanopore
Technologies.