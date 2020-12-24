## Setup

### Required Software

Use of Conda is recommended for environment management.
Requirements include `Kraken2`, `Snakemake`, and their dependencies. For this we provide a conda environment file that can be created with the following command:

`conda env create --file envs/rarefaction_pipe.txt`

`Krakefaction` is another requirement which is available from https://github.com/phac-nml/krakefaction.
After cloning the repository, replace `krakefaction/krakefaction/Krackfaction.py` with our patched copy found at `metagenomics_rarefaction/setup/Krakefaction.py`. After replacing this, execute the bash script `krakefaction/INSTALL.sh`. Installation options are also available and are described in the README. 
Ensure that the executable `krakefaction` is available from PATH, appending it to your PATH file if needed.

### Data Setup

__1.__ Ensure that input kraken2 classification output files are organized as desired within `metagenomics_rarefaction/data/`.
    * More detail about data organization including managing separate pipeline runs found in `metagenomics_rarefaction/data/README.md`.

__2.__ Ensure that the kraken2 database that was used for classification is available in `metagenomics_rarefaction/databases/`.

__3.__ Ensure that the `config.yaml` is edited accordingly for database name, filter targets, and data organization. Details are found in the given template file.

Note that symbolic links to original directories works for data and database.