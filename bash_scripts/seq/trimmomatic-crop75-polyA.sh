#!/bin/bash
mkdir trimmed-crop75-polyA

for fq1 in *1.fastq.gz; do
  fq2=${fq1%%1.fastq.gz}'2.fastq.gz'
  echo $fq1
  echo $fq2
  echo ${fq1%%_1.fastq.gz}'.fastq.gz'
  java -jar /mnt/e/Trimmomatic-0.39/trimmomatic-0.39.jar PE -threads 4 -phred33 $fq1 $fq2 \
  trimmed-crop75-polyA/${fq1%%1.fastq.gz}'trimmed-crop75-polyA_1.fastq.gz' trimmed-crop75-polyA/${fq1%%1.fastq.gz}'trimmed-crop75-polyA_1U.fastq.gz' trimmed-crop75-polyA/${fq2%%2.fastq.gz}'trimmed-crop75-polyA_2.fastq.gz' trimmed-crop75-polyA/${fq2%%2.fastq.gz}'trimmed-crop75_2U.fastq.gz' \
  CROP:75 ILLUMINACLIP:/mnt/e/Trimmomatic-0.39/adapters/TruSeq3-PE-polyA.fa:2:30:10:1:true LEADING:30 TRAILING:30 MINLEN:30
done
