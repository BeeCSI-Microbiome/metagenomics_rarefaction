#!/usr/bin/env python
"""
# =============================================================================
GLOBALS & IMPORTS
# =============================================================================
"""
import os
import logging

# initialize logging
logging.basicConfig(level=logging.DEBUG)
l = logging.getLogger('Log')
c_handler = logging.StreamHandler()
# Change DEBUG to WARNING when testing is finished
c_handler.setLevel(logging.DEBUG)
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
l.addHandler(c_handler)
l.propagate = False

"""
# =============================================================================
# =============================================================================
"""

"""
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Class - TaxonNode
------
PURPOSE
-------
This class represents a node of a taxonomic level, with links to subtaxa and 
supertaxon.
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
"""
class TaxonNode:

    def __init__(self, clade_count, taxa_count, rank, taxid, name, supertaxon=None):
        self.clade_count = int(clade_count) # num of db entries of this + subtaxa
        self.taxa_count = int(taxa_count)   # num of db entries of this exact taxa
        self.rank = rank
        self.taxid = taxid
        self.name = name.strip()
        self.supertaxon = supertaxon        # link to supertaxon node
        self.subtaxa = []                   # list of links to subtaxa nodes

    def check_clade_sum(self):
        """Returns boolean on whether the sum of subtaxa clade_counts equals
           this node's clade_count"""
        return self.clade_count == sum([subtaxon.clade_count for subtaxon in self.subtaxa])

    def __str__(self):
        s = 'Taxon name: {} - Rank {}\n'.format(self.name, self.rank)
        s += '\tTaxa ID: {}\n'.format(self.taxid)
        s += '\tClade count: {}\n'.format(self.clade_count)
        s += '\tTaxa count: {}\n'.format(self.taxa_count)
        s += '\tSupertaxa: {}\n'.format(self.supertaxon)
        s += '\tSubtaxa: {}\n'.format(' '.join([subtaxon.name for subtaxon in self.subtaxa]))
        return s

"""
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
"""


"""
# =============================================================================
MAIN
# =============================================================================
"""
def main():
    """Verify inputs, then run script"""
    # get inspection filename and filtered kraken output file paths from snakemake
    db_inspection, infile_paths = get_inputs()
    run(db_inspection, infile_paths)
    
"""
# =============================================================================
# =============================================================================
"""

def get_inputs():
    """Get the inputs from snakemake.
       Database inspection file, and paths to filtered kraken output files"""
    # retrieve the name of the inspection file from snakemake
    db_inspection = snakemake.input[0]
    l.debug('Name of database inspection file: {}'.format(db_inspection))

    # retrieve the paths of filtered files from snakemake
    infile_paths = snakemake.input[1:]
    l.debug('{} input files were received from snakemake'.format(len(infile_paths)))

    # verifiy files
    check_file_existence(db_inspection, infile_paths)

    return(db_inspection, infile_paths)


def check_file_existence(db_ins, in_paths):
    """Validate file existence, raising error upon failure"""
    # check database inspection file
    if not os.path.isfile(db_ins):
        l.error('The database inspection file "{}" was not found'.format(db_ins))
        raise RuntimeError(
            "ERROR: could not open database inspection file {}\n".format(db_ins))
    
    # check each kraken input file
    for f in in_paths:
        if not os.path.isfile(f):
            l.error('The input file "{}" was not found'.format(f))
            raise RuntimeError(
                "ERROR: could not open input file {}\n".format(f))

    l.debug('All input files were located')
    return
        

def run(db_inspection, infile_paths):
    """Main logical control of the script occurs within"""
    taxon_tree = get_taxon_tree(db_inspection)
    

def get_taxon_tree(db_ins):
    """Produce a taxonomy tree for retrieving lineages of reads"""
    # get database inspection file as list of lines
    with open(db_ins, 'r') as f:
        inspection_lines = f.readlines()
    l.debug('Head of inspection file {}'.format(inspection_lines[:5]))

    
    # create root node
    root_line = inspection_lines[0].split('\t')
    root_node = TaxonNode(*root_line[1:])
    l.debug(root_node)
    

    for taxon in [line.split('\t') for line in inspection_lines[1:]]:
        pass
        

    return ''


if __name__ == '__main__':
    main()
