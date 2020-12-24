# Data Directory

##### 11/17/2020

This directory is where you should store the data to be used with the pipeline.

You may separate different pipeline runs by creating subdirectories here and specifying the directory names in the config.yaml before running snakemake. You may also separate data groups by using subdirectories (and adjusting the config.yaml file accordingly).

**e.g.**

> I want to perform a new run of the pipeline and separate the data into shallow and deep categories. I will name this run `new-run`

> In this directory I make subdirectory named `new-run`, and within `new-run` I create 2 subdirectories `shallow` and `deep`, within which I place my Kraken2 output files.

> In the config.yaml file under the data: list, I include 2 lines specifying the location of the data within this `data/` directory: `new-run/shallow` and `new-run/deep`

The benefit of this method of data separation is that for each intermediate step, and the final results, the intermediate/resulting data will be separated in the same way. So the final rarefied results will be in found in the directory `rarefied/new-run/shallow`, etc.
