# Retrieve fasta sequence from the local blast database

With standalone [blast](https://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Web&PAGE_TYPE=BlastDocs&DOC_TYPE=Download) you can produce local blast database from a fasta file of your choice and blast a query sequence against it. 


The following script is used to retrieve the fasta sequence of the best blast hit or region around it from the local blast database. 

### 0. Creating local blast database
You can create the local databases with the following command. For compatibility with the downstream script, make sure that the namings of the resulting databases have the prefix "blastdb.SampleName", and the same sample names are used in the downstream script. The databases are created once and can be reused. 

```bash
for sample in fDanAlb1 fDanCho1 fDanDra1 fDanJai1 fDanKya3 fDanTin1 fDanTra1 fDreABz2 fDreCBz1 fDreNAz1
do
makeblastdb -in $sample.purged.renamed.clipped.fa -dbtype nucl -out blastdbs/blastdb.$sample -parse_seqids &
done

```
### 1. Prepare json input file 
To describe the input files (i.e. query sequence, samples/databases to search) and blast parameters use a [json](https://json.org/example.html) file. Here is an example:

```
{
	"prefix":"obe",
	"samples": ["fDanAes4", "fDanAlb1", "fDanKya3", "fDreABz2"],
	"query": "query_sequences/kcnj13_exon7.fa",
	"range":[0, 5000],
	"defaults": {
		"samples":["fDanAes4", "fDanAlb1", "fDanCho1", "fDanJai1", "fDanKya3", "fDanTin1", "fDreABz2", "fDreCBz1", "fDreNAz1", "Trinity_aesculapii", "grcz11"], 
		"eval": "1e-100",
		"db-path": "/ebio/ecnv_projects/common_resourses/data/spp_blastdb/",
		"range":[]
	}
}

```
You are expected to provide following parameters:
* "prefix" : a string that you want to be used as a prefix for the output files. REQUIRED, no defaults provided
* "samples" : list of strings, naming the samples. Should be the same as those used for blast database creation. If none provided, will use the default list of samples (for eCNV group)
* "query" : path to query sequence in fasta format. REQUIRED, no defaults provided
* "eval" : e-value cut-off for blast hits. Default: "1e-100"
* "db-path" : path to the folder containing blast databases. If none provided, will use the default (for eCNV group)
* "range" : used to determine which sequence range around the blast hit to retrieve:
  - if none provided, will use the default [] (empty list) and extract exactly the aligned sequence found by blast search
  - if you provide a range [start, end], you will retrieve the sequence in relation to the first base of blast hit. [-50, 700] will return the sequence from 50 bases upstream to 700 bases downstream of blast hit start.
    - use negative numbers to specify the range upstream of blast hit start
    - use positve numbers to specify the range downstream of blast hit start


### 2. Run blast search and check the results 

Use the following command to blast the query sequence against the local blast databases. The output of the command will save the blast best hit as a pairwise sequence alignment for each blast database (as defined by sample list of the input_parameters.json file) in the current working directory. The output files will be named like prefix.sample.out. Check, if you get the alignment you expect. If not, change e-value cutoff accordingly. 

```bash
python3 blast_inspection.py sample_input.json
#or
python3 /path/to/blast_inspection.py /another/path/to/sample_input.json
#the output files will be saved in your working directory
```
If you are satisfied with blast output, you can...

### 3. Retrieve fasta from the local databases

The following command will save the sequence range (as specified by "range" parameter in the input parameters json file) from the local database as a fasta sequence in your working directory. The output files will be named like prefix.sample.fa. prefix.fa file contains sequences from all samples with sample name as a fasta header.

``` bash
python3 retrieve_fasta.py sample_input.json
#or
python3 /path/to/retrieve_fasta.py /another/path/to/sample_input.json
#the output files will be saved in your working directory
```

### 4. Run blast of multiple sequences contained in single fasta file

Equivalent to blast_inspection.py, but with multiple fasta sequences provided in a single file as an input. Returns alignments in default blast format.

``` bash
python3 blast_inspection_multifasta.py sample_input.json input_fasta.fa
#or
python3 /path/to/blast_inspection_multifasta.py /another/path/to/sample_input.json /path/to/input_fasta.fa
#the output files will be saved in your working directory
```
