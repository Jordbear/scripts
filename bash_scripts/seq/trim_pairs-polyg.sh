#!/bin/bash
mkdir fastq_trimmed
for fq1 in *1.fastq.gz; do
  fq2=${fq1%%1.fastq.gz}'2.fastq.gz'
  echo $fq1
  echo $fq2
  echo ${fq1%%.fastq.gz}'_trim.fastq.gz'
  echo ${fq2%%.fastq.gz}'_trim.fastq.gz'
  cutadapt -j 4 -q 30 -m 50 -a AGATCGGAAGAGC -a GGGGGGGGGGGGG -A AGATCGGAAGAGC -A GGGGGGGGGGGGG --trim-n -o fastq_trimmed/${fq1%%.fastq.gz}'_trim'${fq1##*1} -p fastq_trimmed/${fq2%%.fastq.gz}'_trim'${fq2##*2} $fq1 $fq2
done
