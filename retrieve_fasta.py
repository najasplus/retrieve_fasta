# -*- coding: utf-8 -*-
"""
Created on Sat Feb 16 14:24:19 2019

@author: Anastasia
"""

#!/usr/bin/python3

import json
import os
import sys 


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
    if "range" in data:
        sequence_range = data["range"]
    else:
        sequence_range = data["defaults"]["range"]

    return samples, e_val, db_path, query, prefix, sequence_range

def coordinate_in_valid_range(coord):
    if coord < 1:
        return(False)
    else:
        return(True)

def retrieve_fasta_range(tmp_file, sequence_range):
    with open(tmp_file) as f:
        coordinates = f.readlines()[0].split("\t")
        #print(coordinates)
        
        #find out if we are on the forward or reverse strand
    plus_strand = True
    alignment_start = int(coordinates[8])
    alignment_end = int(coordinates[9])
    
    #print(alignment_start, alignment_end)
    
    range_list_length = len(sequence_range)
    
    if alignment_start > alignment_end:
        plus_strand = False
    
    if range_list_length == 0 and plus_strand:
        sequence_start = alignment_start
        sequence_end = alignment_end
    elif range_list_length == 0 and not plus_strand:
        sequence_start = alignment_end
        sequence_end = alignment_start
              
    elif range_list_length >= 2 and plus_strand:
        sequence_start = alignment_start + min(sequence_range)
        sequence_end = alignment_start + max(sequence_range)
        if range_list_length > 2:
            print("WARNING: You have more than two values defining sequence range. \n"
                  "Only minimum and maximum values will be used")
    elif range_list_length >= 2 and not plus_strand:
        sequence_end = alignment_start - min(sequence_range)
        sequence_start = alignment_start - max(sequence_range)
        if range_list_length > 2:
            print("WARNING: You have more than two values defining sequence range. \n"
                  "Only minimum and maximum values will be used")
    else:
        raise Exception("Range parameter should have 2 values or no value")

    if not coordinate_in_valid_range(sequence_start):
        sequence_start = 1
    if not coordinate_in_valid_range(sequence_end):
        sequence_end = 1


     
    contig = coordinates[1]
    return contig, sequence_start, sequence_end, plus_strand


if len(sys.argv) != 2:
    #print("Please provide exactly one file as parameter input")
    raise Exception("Please provide exactly one file as parameter input")


with open(sys.argv[1], encoding='utf-8', strict = False) as f:
    data = json.load(f)


samples, e_val, db_path, query, prefix, sequence_range = parse_parameters(data)

blast_command = ("blastn -db {db_path}blastdb.{sample} -query {query} "
                "-evalue {e_val} -num_alignments 1 -outfmt 6 -out tmp.6out")

fasta_plus = ("blastdbcmd -db {db_path}blastdb.{sample} "
              "-entry {contig} -range {sequence_start}-{sequence_end} "
              "-out {prefix}.{sample}.fa")

fasta_minus = ("blastdbcmd -db {db_path}blastdb.{sample} "
              "-entry {contig} -range {sequence_start}-{sequence_end} "
              "-strand 'minus' -out {prefix}.{sample}.fa")

fo = open(prefix + ".fa", "a")

for sample in samples:
    command_line = blast_command.format(db_path = db_path, 
                                        sample = sample, 
                                        query = query, 
                                        e_val = e_val)
    print(sample)
    print(command_line)
    os.system(command_line)
    
    contig, sequence_start, sequence_end, plus_strand = retrieve_fasta_range("tmp.6out", sequence_range)
    if plus_strand:
        fasta_command = fasta_plus.format(db_path = db_path,  sample = sample,
                                          sequence_start = sequence_start, sequence_end = sequence_end,
                                          contig = contig, prefix = prefix)
    else:
        fasta_command = fasta_minus.format(db_path = db_path,  sample = sample,
                                          sequence_start = sequence_start, sequence_end = sequence_end,
                                          contig = contig, prefix = prefix)
    print(fasta_command)
    os.system(fasta_command)
    os.system("rm tmp.6out")
    with open("{prefix}.{sample}.fa".format(prefix = prefix, sample = sample)) as f:
        fasta_single = f.readlines()
        fo.writelines(">"+sample + "\n")
        for line in fasta_single[1:]:
            fo.writelines(line)

fo.close()    
        
    