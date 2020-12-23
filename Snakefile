import glob

# Read in variables from config file
configfile: "config.yaml"
DATAPATHS=config["datapaths"]
DB="database/{}".format(config["db"])
FILTER_TARGETS=config["filter_targets"]
SAMPLES = []

# Get the sample base names (no extensions) with or without subdirectories as groups
if DATAPATHS:
	for datapath in DATAPATHS:
		SAMPLES.extend([path.replace("data/", "").split(".")[0] for path in glob.glob("data/{}/*".format(datapath))])
else:
	SAMPLES.extend([path.replace("data/", "").split(".")[0] for path in glob.glob("data/*")])
# Display samples
print("Running with the following samples:\n\t{}".format("\n\t".join(SAMPLES)))

# create the filter string based on config file
F_STRING="unclassified\|cellular organism"
if FILTER_TARGETS:
	F_STRING = F_STRING + "\|" + "\|".join(FILTER_TARGETS)
print("Filtering with the following filter string:\n\t'{}'".format(F_STRING))



rule all:
	input:
		expand("rarefied/{sample}.csv", sample=SAMPLES)

# filter out unclassifed reads, "cellular organism" reads, and all others specified
# in the config file
rule filter:
	input:
		"data/{sample}.txt"
	output:
		"filtered/{sample}_filtered.txt"
	threads: 1
	shell:
		"cat {input} | grep -v \"" + F_STRING + "\" > {output}"

# Get the db_inspection file needed for the translate step
rule get_db_inspection:
    input:
        DB
    output:
        "db_inspection.txt"
    shell:
        "kraken2-inspect --db {input} > db_inspection.txt"

# custom translate script is used to produce the translated read files needed
# for krakefaction
rule translate:
	input:
		db_inspection = "db_inspection.txt",
		readfiles = expand("filtered/{sample}_filtered.txt", sample=SAMPLES)
	output:
		expand("translated/{sample}_translated.txt", sample=SAMPLES)
	script:
		"scripts/kraken2-translate.py"

# perform rarefaction
rule krakefaction:
	input:
		trans="translated/{sample}_translated.txt",
		untrans="filtered/{sample}_filtered.txt"
	output:
		"rarefied/{sample}.csv"
	shell:
		"krakefaction -u {input.untrans} -t {input.trans} -o {output}"

#TODO: add R scripts for producing plots?
