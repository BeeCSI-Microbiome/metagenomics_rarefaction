#!/usr/bin/env python
"""
# =============================================================================
GLOBALS & IMPORTS
# =============================================================================
"""
import os
import logging
from collections import deque

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
        self.rank = rank.lower()
        self.taxid = taxid
        self.name = name.strip()
        self.supertaxon = supertaxon        # link to supertaxon node
        self.subtaxa = []                   # list of links to subtaxa nodes
        self.subtaxa_sum = int(taxa_count)

    def check_clade_sum(self):
        """Returns boolean on whether the sum of subtaxa clade_counts equals
           this node's clade_count"""
        return self.clade_count == sum([subtaxon.clade_count for subtaxon in self.subtaxa])

    def add_child(self, subtaxon):
        """Add a subtaxon child node to this node
           Add the new node's taxa_count to the subtaxa_sum of all supertaxa"""
        # add to parent's subtaxa list
        self.subtaxa.append(subtaxon)
        # add parent as child's supertaxa
        subtaxon.supertaxon = self

        if subtaxon.taxa_count != 0:
            # add tax_count to parent's sum
            self.subtaxa_sum += subtaxon.taxa_count

            curr_parent = self
            # add to any further ancestor's sums
            while curr_parent.supertaxon is not None:
                curr_parent = curr_parent.supertaxon
                curr_parent.subtaxa_sum += subtaxon.taxa_count
        
        l.debug('Made following node child of next node:\n{}\n{}'.format(subtaxon, self))

        return


    def has_full_subtaxa(self):
        """Return boolean whether all subtaxa have been added to this node"""
        return self.subtaxa_sum == self.clade_count

    def __str__(self):
        s = 'Taxon name: {} - Rank {}\n'.format(self.name, self.rank)
        s += '\tTaxa ID: {}\n'.format(self.taxid)
        s += '\tClade count: {}\n'.format(self.clade_count)
        s += '\tTaxa count: {}\n'.format(self.taxa_count)
        if self.supertaxon is not None:
            s += '\tSupertaxa: {}\n'.format(self.supertaxon.name)
        s += '\tSubtaxa sum: {}\n'.format(self.subtaxa_sum)
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
    taxon_dict = create_taxon_dict(db_inspection)
    

def create_taxon_dict(db_ins):
    """Produce a taxonomy dictionary with taxids as keys and lineage strings as values"""
    # get database inspection file as list of lines
    with open(db_ins, 'r') as f:
        inspection_lines = f.readlines()
    l.debug('Head of inspection file {}'.format(inspection_lines[:5]))

    root = create_tree(inspection_lines)    

    return ''


def create_tree(inspection_lines):
    """Create the taxonomy tree and return the root node"""
    # make deque for leftpopping of inspection lines
    inspection_lines = deque(inspection_lines)
    
    # create root node
    root_line = inspection_lines.popleft().split('\t')
    root_node = TaxonNode(*root_line[1:])
    l.debug('Create root node:\n{}'.format(root_node))

    # stack for tracking nodes with more subtaxa to add
    stack = []
    stack.append(root_node)

    # while there are still lines to make nodes from
    while inspection_lines:
        # get the node at the top of the stack
        curr_node = stack[-1]
        # create new taxon node
        new_node = TaxonNode(*inspection_lines.popleft().split('\t')[1:])
        l.debug('Creating node for {}'.format(new_node.name))
        
        # if current node has full subtaxa list, pop stack until otherwise
        if curr_node.has_full_subtaxa():
            curr_node = find_next_parent(stack)

        # add the new node to the parent node
        curr_node.add_child(new_node)
        l.debug('Adding {} as direct subtaxa of {}'.format(new_node.name, curr_node.name))
        # put new node on top of stack if it still needs subtaxa
        if not new_node.has_full_subtaxa:
            stack.append(new_node)
            l.debug('Putting {} on top of stack'.format(new_node.name))
    
    return root_node
    

def find_next_parent(stack):
    """Pops stack until a node that still needs children is found"""
    node = stack.pop()
    l.debug('Popping node:\n{}'.format(node))
    if not node.has_full_subtaxa():
        return node
    else:
        return find_next_parent(stack)



if __name__ == '__main__':
    main()
