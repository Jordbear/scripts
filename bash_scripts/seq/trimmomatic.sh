#!/bin/bash
mkdir trimmed

for fq1 in *1.fastq.gz; do
  fq2=${fq1%%1.fastq.gz}'2.fastq.gz'
  echo $fq1
  echo $fq2
  java -jar /mnt/e/Trimmomatic-0.39/trimmomatic-0.39.jar PE -threads 4 -phred33 $fq1 $fq2 \
  trimmed/${fq1%%1.fastq.gz}'trimmed_1.fastq.gz' trimmed/${fq1%%1.fastq.gz}'trimmed_1U.fastq.gz' trimmed/${fq2%%2.fastq.gz}'trimmed_2.fastq.gz' trimmed/${fq2%%2.fastq.gz}'trimmed_2U.fastq.gz' \
  ILLUMINACLIP:/mnt/e/Trimmomatic-0.39/adapters/TruSeq3-PE.fa:2:30:10:1:true LEADING:30 TRAILING:30 MINLEN:30
done
