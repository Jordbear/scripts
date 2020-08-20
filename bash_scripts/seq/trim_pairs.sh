#!/bin/bash
mkdir trimmed
for fq1 in *1.fastq.gz; do
  fq2=${fq1%%1.fastq.gz}'2.fastq.gz'
  echo $fq1
  echo $fq2
  echo ${fq1%%1.fastq.gz}'trimmed_1.fastq.gz'
  echo ${fq2%%2.fastq.gz}'trimmed_2.fastq.gz'
  cutadapt -j 4 -q 30 -m 50 -a AGATCGGAAGAGC -A AGATCGGAAGAGC --trim-n -o trimmed/${fq1%%1.fastq.gz}'trimmed_1.fastq.gz' -p trimmed/${fq2%%2.fastq.gz}'trimmed_2.fastq.gz' $fq1 $fq2
done
