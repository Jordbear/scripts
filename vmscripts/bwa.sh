#!/bin/bash
ref_index=/data/references/mm10-base_spikes/bwa_index/mm10-basespikes.fa
threads=`nproc --all`
echo Aligning read pairs to reference index: ${ref_index}
mkdir aligned

for fq1 in *R1*.fastq.gz; do
  fq2=${fq1/R1/R2}
  bam=${fq1/R1_/}
  bam=${bam%%.fastq.gz}'.bam'
  echo $fq1
  echo $fq2
  echo $bam
  bwa mem -t $threads $ref_index $fq1 $fq2 | samtools sort -@ $threads -O BAM > aligned/$bam
done
