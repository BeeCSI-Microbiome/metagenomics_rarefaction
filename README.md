# Rarefaction Pipeline

The function of this pipeline is to take `Kraken2` classification results, filter out given taxa, perform rarefaction using `Krakefaction`, and to concatenate results into a single .csv file.

## Setup

### Required Software

Command line R (statistics software) is required for concatenation of results.

#### Conda Environment

Use of Conda is recommended for environment management.
Requirements include `Kraken2`, `Snakemake`, and their dependencies. For this we provide a conda environment file that can be created with the following command:

`conda env create --file envs/rarefaction_pipe.txt`

Activate the Conda environment with the following comming:

`conda activate rarefaction_pipe`

#### Krakefaction

`Krakefaction` is another requirement which is available from [Github](https://github.com/phac-nml/krakefaction).
After cloning the repository, replace `krakefaction/krakefaction/Krackfaction.py` with our patched copy found at `setup/Krakefaction.py`. After replacing this, execute the bash script `krakefaction/INSTALL.sh`. Installation options are also available and are described in the README. 
Ensure that the executable `krakefaction` is available from PATH, appending it to your PATH file if needed.

### Data Setup

__1.__ Ensure that input kraken2 classification output files are organized as desired within `data/` and that all input files end with `_classification.txt`.

 * More detail about data organization including managing separate pipeline runs found in `data/README.md`.

__2.__ Ensure that the kraken2 database that was used for classification is available in `databases/`.

Note that symbolic links to original directories works for data and database.

__3.__ Ensure that the `config.yaml` is edited accordingly for database name, filter targets, and data organization. Details are found in the given template file.



## Usage 

Once all setup is complete, from within `metagenomics_rarefaction/`, run snakemake with the following command:

`snakemake`

See snakemake documentation for pipeline execution options (link below).

## Useful Links

* [Snakemake documentation](https://snakemake.readthedocs.io/en/stable/)
    * [Snakemake options](https://snakemake.readthedocs.io/en/stable/executing/cli.html)
* [Kraken2](https://ccb.jhu.edu/software/kraken2/)
    * [Kraken2 Manual (Github)](https://github.com/DerrickWood/kraken2/wiki/Manual)
* [Krakefaction (Github)](https://github.com/phac-nml/krakefaction)
* [YAML file syntax](https://docs.ansible.com/ansible/latest/reference_appendices/YAMLSyntax.html)

## Workflow

![Workflow](/images/rarefaction_pipeline_workflow.png)

__1.__ Filter out unclassified reads, root taxa ranks, and any filter targets specified in `config.yaml`. This set takes as input the data paths specified in `config.yaml`. Filtered files are are saved in `filtered/`.

__2.__ Produce a database inspection file utilizing the kraken2 script `kraken2-inspect`, which requires the kraken2 database specified in `config.yaml`. This saves as `metagenomics_rarefaction/db_inspection`

__3.__ Run python script `scripts/kraken2-translate.py`, which requires filtered files and database inspection file. Translated files are saved in `translated/`.

__4.__ Perform rarefaction using `krakefaction`, which requires filtered files and translated files. Resulting rarefaction tables are saved in `rarefied/`.

__5.__ Concatenate rarefaction tables using R script `scripts/rarefaction_concat.R`. Final concatenated rarefaction table is saved in `results/` and titled `rarefaction_concat.csv`.

Rarefaction plotting can be done with the resulting concatenated file in R or other plotting software that works with .csv files.

__TODO__: Incorporate R script that produces rarefaction curves into the pipeline

### Cleanup

The following is a list of files that were temporary and are considered removable:

* Filtered files in `filtered/`. (These files can be large if large input files are given)
* Translated files in `translated/`.
* Rarefaction tables in `rarefied/` if the concatenated table is all you need.

