#!/bin/bash
mkdir genes
genes=/mnt/e/ref_bacteria/E_coli_ATCC_8739/Escherichia_coli_ATCC_8739_genes_nuc.bed

for bam in *.bam; do
  echo $bam
  bedtools coverage -a $genes -b $bam -mean > genes/${bam%%.bam}'_genes.tsv'
done
