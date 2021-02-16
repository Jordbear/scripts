#!/bin/bash
ref_index=/pipeline/scratch/jordan/bs/human/Homo_sapiens.GRCh38.dna_sm.primary_assembly-base_spikes_pUC19.fa
threads=`nproc --all`
echo Aligning read pairs to reference index: ${ref_index}
mkdir aligned

for fq1 in *R1*.f*q.gz; do
  fq2=${fq1/R1/R2}
  fq2=${fq2/_val_1/_val_2}
  bam=${fq1/_R1/}
  bam=${bam/_val_1/}
  bam=${bam%%.f*q.gz}.bam
  echo $fq1
  echo $fq2
  echo $bam
  bwameth.py --threads $threads --reference $ref_index $fq1 $fq2 | samtools sort -@ $threads -O BAM > aligned/$bam
done
