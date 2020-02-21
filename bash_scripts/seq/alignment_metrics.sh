#!/bin/bash

mkdir qc

ref=/mnt/e/ref_bacteria/Pseudomonas_aeruginosa_PAO1.fasta

for bam in *.bam; do
  echo $bam
  java -jar /mnt/e/picard.jar CollectAlignmentSummaryMetrics \
  R=$ref \
  I=$bam \
  O=qc/${bam%%.bam}'_alignment.tsv'
done
