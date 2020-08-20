#!/bin/bash
ref=/mnt/e/ref_human/hisat2_GRCh38/GRCh38.dna_sm.primary_assembly
echo Aligning read pairs to reference: ${ref}

mkdir bams
for fq1 in *1.fastq.gz; do
  fq2=${fq1%%1.fastq.gz}'2.fastq.gz'
  echo $fq1
  echo $fq2
  echo ${fq1%%_1.fastq.gz}'.bam'
  hisat2 -q -p 4 -x $ref -1 $fq1 -2 $fq2 | samtools sort -O BAM > bams/${fq1%%_1.fastq.gz}'.bam'
done
