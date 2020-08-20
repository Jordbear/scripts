#!/bin/bash
ref_index=/Users/jordanbrown/sequencing/reference_genomes/spikes/bowtie2_index/spikes
echo Aligning to: ${ref_index}

mkdir bams
echo Aligning read pairs to reference: ${ref_index}
for fq1 in *R1*.fastq.gz; do
  fq2=${fq1/R1/R2}
  bam=${fq1/R1_/}
  bam=${bam%%.fastq.gz}'.bam'
  echo $fq1
  echo $fq2
  echo $bam
  bowtie2 -q -p 6 -X 1000 -x $ref_index -1 $fq1 -2 $fq2 | samtools sort -@ 6 -O BAM > bams/$bam
done
