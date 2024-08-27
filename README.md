
# ONT-Spectre - Long read CNV caller

ONT-Spectre is a tool for calling copy number variations (CNVs) from long-read sequencing data. It uses a combination of read depth and SNV information to call CNVs. The tool is designed to work with Oxford Nanopore Technologies (ONT) data and is optimized for the analysis of human genomes.

## Installation
Recommended ways of installation are using pip or conda or pip package:

```
pip install ont-spectre

```

or

```
conda install nanoporetech::ont-spectre
```

## How to run

Spectre requires as input:
- The result of Mosdepth (directory)
- Reference genome (can be bgzip compressed)
- Window size used in Mosdepth (Make sure the binsize between Mosdepth and Spectre are matching. We suggest a binsize of 1000 base pairs.)
- VCF file containing SNV

> INFO: Make sure to include "/" at the end if you are adding directory paths.


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
