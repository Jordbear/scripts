scripts by Jordbear

---------------------------------------
1. Overview
---------------------------------------
This repository consists of a number of scripts developed for various purposes.

---------------------------------------
2. Use in analysis of DNA sequencing data
---------------------------------------
Many of the Bash scripts were written to automate the processing of DNA sequencing data using free and open-source bioinformatics tools. The tools utilised include, but may not be limited to: Trimmomatic, Bowtie2, HISAT2, Samtools, Picard and Bedtools. Where applicable these tools will need to be installed in order to successfully run the scripts. It is highly recommended to add directories containing scripts of use to the PATH variable so that they can be easily called by a Bash terminal.

Many of the Python scripts were written to collate and plot data from the output of processing. These scripts require Python3 and various packages to run including, but not necessarily limited to: NumPy, Pandas, Glob, Matplotlib and Seaborn. These packages will need to be installed in the relevant Python3 environment in order for the scripts to run successfully. It is highly recommended to add directories containing scripts of use to the PATH variable so that they can be easily called by a Bash terminal or by Bash scripts from this repositiry.

For convenience sever comprehensive Bash scripts and their assosciated Python3 scripts are duplicated together in /seq. Adding this directory to your $PATH variable will allow oyu to run these anywhere from the command line.