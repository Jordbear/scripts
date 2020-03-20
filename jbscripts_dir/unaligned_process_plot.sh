#!/bin/bash
mkdir unaligned
for fq1 in *1.fastq.gz; do
  fq2=${fq1%%1.fastq.gz}'2.fastq.gz'
  echo $fq1
  echo $fq2
  echo ${fq1%%_1.fastq.gz}'.bam'
  java -jar $PICARD FastqToSam \
  F1=$fq1 \
  F2=$fq2 \
  O=unaligned/${fq1%%_1.fastq.gz}'_unaligned.bam' \
  SM=${fq1%_*_1.fastq.gz} \
  SORT_ORDER=coordinate
done
cd unaligned

mkdir qc
for bam in *.bam; do
  echo $bam
  java -jar $PICARD CollectAlignmentSummaryMetrics \
  I=$bam \
  O=qc/${bam%%.bam}'_alignment.tsv'
done
cd qc

directory=$(which jbscripts)_dir/
${directory}alignment.py
