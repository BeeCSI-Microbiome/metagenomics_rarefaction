import os
import glob

#def get_filtered():
#        filenames = [os.path.basename(f) for f in glob.glob('Kraken_filtered*.tabular')]
#        return sorted(filenames)
#
#def get_translated():
#        filenames = [os.path.basename(f) for f in glob.glob('Kraken_translated*.tabular')]
#        return sorted(filenames)

#def output_samples():
#        filenames = [os.path.splitext(f)[0] for f in glob.glob('Kraken_translated*.tabular')]
#        samples = ['RF_'+f.split('_')[3] for f in filenames]
#        return sorted(samples)

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

