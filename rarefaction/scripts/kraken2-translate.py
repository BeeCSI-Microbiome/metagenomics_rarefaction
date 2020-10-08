#!/usr/bin/env python

import os

pID = 'TRANSLATION STEP:'

"""
# =============================================================================
MAIN
# =============================================================================
"""
def main():
    # retrieve the name of the inspection file from snakemake
    db_inspection = snakemake.input[0]
    print(pID, db_inspection)

    # retrieve the paths of filtered files from snakemake
    infile_paths = snakemake.input[1:]
    print(pID, len(infile_paths))

    # check file existence
    print(pID, 'current directory:', os.getcwd)
    print(pID, 'does {} exist'.format(db_inspection), os.path.isfile(db_inspection))
    


"""
# =============================================================================
# =============================================================================
"""


if __name__ == '__main__':

    main()