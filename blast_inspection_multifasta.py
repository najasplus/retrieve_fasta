# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 12:27:17 2019

@author: Anastasia
Split fasta files and run blast inspection for all sequences in fasta
"""

#!/usr/bin/python 

import json
import os
import sys 

json_input = sys.argv[1]
fasta_input = sys.argv[2]

def write_tmp_query(fasta, index):
    fasta_seq = fasta[1::2]
    fasta_headers = fasta[0::2]
    
    fo = open("tmp.fa", "w+")
    fo.writelines((fasta_headers[index]+ fasta_seq[index]))
    fo.close()
        

def parse_parameters(data):
    if "samples" in data:
        samples = data["samples"]
    else:
        samples = data["defaults"]["samples"]
    if "eval" in data:
        e_val = data["eval"]
    else:
        e_val = data["defaults"]["eval"]
    if "db-path" in data:
        db_path = data["db-path"]
    else:
        db_path = data["defaults"]["db-path"]
    if "query" in data:
        query = data["query"]
    else:
        raise Exception("Query sequence is missing")
    if "prefix" in data:
        prefix = data["prefix"]
    else:
        raise Exception("Prefix for filename is missing")

    return samples, e_val, db_path, query, prefix

def blast_inspection(db_path, samples, query, e_val, prefix):
    """generate blast outputs in default format from """
    blast_command = ("blastn -db {db_path}blastdb.{sample} -query {query} "
                    "-evalue {e_val} -num_alignments 1 -outfmt 0 -out "
                    "{prefix}.{sample}.results.out")
    
    for sample in samples:
        command_line = blast_command.format(db_path = db_path, 
                                            sample = sample, 
                                            query = query, 
                                            e_val = e_val, 
                                            prefix = prefix)
        print(command_line)
        os.system(command_line)

def run_pipeline(json_input, fasta_input):
    with open(fasta_input) as f:
        fasta = f.readlines()
    
    with open(json_input) as f:
        data = json.load(f)
    
    samples, e_val, db_path, query, prefix = parse_parameters(data)
    
    for i in range(int(len(fasta)/2)):
        prefix_new = prefix + str(i)
        write_tmp_query(fasta, i)
        query = "tmp.fa"
        blast_inspection(db_path, samples, query, e_val, prefix_new)

run_pipeline(json_input, fasta_input)



    
    
    
