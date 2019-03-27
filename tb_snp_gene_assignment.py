#!/usr/bin/env python


import sys
import argparse
import re
import pandas as pd
import pickle
#import math
import numpy as np


def load_obj(name ):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def Parser():
    the_parser = argparse.ArgumentParser(description="add label to first line of file")
    the_parser.add_argument('--input', required=True, action="store", type=str, help="input file")
    the_parser.add_argument('--output', required=True,  action="store", type=str, help="output file path")
    args = the_parser.parse_args()
    return args
  
def main():

    args=Parser()

    forward_features = load_obj('forward_features')
    reverse_features = load_obj('reverse_features')
    if args.input.endswith('.gz'):
        input = pd.read_csv(args.input, compression='gzip', header=0, sep='\t')
    else:
        input = pd.read_csv(args.input, header=0, sep='\t')
    output = input.copy()
    output = output.replace(np.nan, '', regex=True)
    for index, row in output.iterrows():
        ref_pos = row['REFPOS']
        nuc_change = re.sub('[0-9\-]','',row['NUCHANGE'])
        new_gene_name = ''
        new_gene_id = ''
        new_nuc_change = ''
        if type(forward_features[ref_pos]) != int:
            for i in forward_features[ref_pos]:
                new_gene_name = new_gene_name + i[0] + ', '
                if type(i[1]) == float:
                    new_gene_id = new_gene_id + str(i[4]) + ', '
                else:
                    new_gene_id = new_gene_id + str(i[1]) + ', '
                rel_pos = ref_pos - i[2] + 1
                new_nuc_change = new_nuc_change + str(rel_pos) + nuc_change + ','
        if type(reverse_features[ref_pos]) != int:
            for i in reverse_features[ref_pos]:
                new_gene_name = new_gene_name + i[0] + ', '
                if type(i[1]) == float:
                    new_gene_id = new_gene_id + str(i[4]) + ', '
                else:
                    new_gene_id = new_gene_id + str(i[1]) + ', '
                rel_pos = i[3] - ref_pos + 1
                new_nuc_change = new_nuc_change +str(rel_pos) + nuc_change + ', '
        output.at[index,'GENENAME'] = new_gene_name.rstrip(", ")
        output.at[index,'GENEID'] = new_gene_id.rstrip(", ")
        output.at[index,'NUCHANGE'] = new_nuc_change.rstrip(", ")
    output.to_csv(args.output, sep='\t', index = False)

if __name__ == '__main__':
    sys.exit(main())