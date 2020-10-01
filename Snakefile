import os
import glob

SAMPLE = [os.path.basename(f).split('_')[3].split('.')[0] for f in glob.glob('Kraken_translate*.tabular')]

rule all:
    input:
       expand('RF_{sample}.rarefied', sample=SAMPLE)

rule rarefaction:
    input: 
        filtered = 'Kraken_filtered_F_{sample}.tabular',
        translated = 'Kraken_translate_F_{sample}.tabular'
    output:
        'RF_{sample}.rarefied'
    shell:
        'rarefaction -u {input.filtered} -t {input.translated} -o {output}'

