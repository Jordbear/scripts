#!/bin/bash
mkdir trimmed

for fq1 in $(find . -name '*R1*.fastq.gz'); do
  fq2=${fq1/R1/R2}
  fq1f=${fq1##*/}
  fq2f=${fq2##*/}
  echo $fq1
  echo $fq2
  echo ${fq1f}
  echo ${fq2f}
  java -jar /Users/jordanbrown/sequencing/Trimmomatic-0.39/trimmomatic-0.39.jar PE -threads 6 -phred33 $fq1 $fq2 \
  trimmed/${fq1f%%.fastq.gz}'_trimmed.fastq.gz' trimmed/${fq1f%%.fastq.gz}'_trimmedU.fastq.gz' trimmed/${fq2f%%.fastq.gz}'_trimmed.fastq.gz' trimmed/${fq2f%%.fastq.gz}'_trimmedU.fastq.gz' \
  ILLUMINACLIP:/Users/jordanbrown/sequencing/Trimmomatic-0.39/adapters/TruSeq3-PE.fa:2:30:10:1:true LEADING:20 TRAILING:20 MINLEN:30
done
