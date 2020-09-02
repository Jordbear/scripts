#!/bin/bash
ref_index=/data/references/GRCh38-base_spikes/bwa_index/Homo_sapiens.GRCh38.dna_sm.primary_assembly-base_spikes.fa
runid=id
threads=`nproc --all`
echo Aligning read pairs to reference index: ${ref_index}
mkdir aligned

for fq1 in *R1*.fq.gz; do
  fq2=${fq1/R1/R2}
  fq2=${fq2/val_1/val_2}
  bam=${fq1/_R1*val_1/}
  bam=${bam%%.fq.gz}'.bam'
  echo $fq1
  echo $fq2
  echo $bam
  bwa mem -t $threads -R "@RG\tID=$runid\tSM=${bam%.bam}" $ref_index $fq1 $fq2 | samtools sort -@ $threads -O BAM > aligned/$bam
done
