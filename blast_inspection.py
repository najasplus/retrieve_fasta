# -*- coding: utf-8 -*-
"""
Created on Sat Feb 16 10:53:35 2019

@author: Anastasia
"""

#!/usr/bin/python3

import json
import os
import sys 
#data = {}


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
        print("Query sequence is missing")
    if "prefix" in data:
        prefix = data["prefix"]
    else:
        print("Prefix for filename is missing")

    return samples, e_val, db_path, query, prefix

print(sys.argv)

if len(sys.argv) != 2:
    print("Please provide exactly one file as parameter input")
    raise Exception("Please provide exactly one file as parameter input")


with open(sys.argv[1], encoding='utf-8') as f:
    data = json.load(f)

#print(data)

samples, e_val, db_path, query, prefix = parse_parameters(data)

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
#print(prefix, samples)




