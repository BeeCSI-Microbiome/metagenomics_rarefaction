#!/usr/bin/env python
"""
# =============================================================================
GLOBALS & IMPORTS
# =============================================================================
"""
import os
import logging

# initialize logging
l = logging.getLogger(__name__)
c_handler = logging.StreamHandler()
# Change DEBUG to WARNING when testing is finished
c_handler.setLevel(logging.DEBUG)
l.addHandler(c_handler)

pID = 'TRANSLATION STEP:'
"""
# =============================================================================
# =============================================================================
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

    taxon_tree = get_taxon_tree(db_inspection)
    
"""
# =============================================================================
# =============================================================================
"""

def get_inputs():
    """Get the inputs from snakemake.
       Database inspection file, and paths to filtered kraken output files"""
    # retrieve the name of the inspection file from snakemake
    db_inspection = snakemake.input[0]
    l.debug(pID, db_inspection)

    # retrieve the paths of filtered files from snakemake
    infile_paths = snakemake.input[1:]
    l.debug(pID, len(infile_paths))

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
        

def get_taxon_tree(db_ins):
    return ''


if __name__ == '__main__':
    main()
