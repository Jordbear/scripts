#!/bin/bash
ref_index=/data/references/GRCh38-base_spikes/bwa_index/Homo_sapiens.GRCh38.dna_sm.primary_assembly-base_spikes.fa
runid=id
threads=`nproc --all`
echo Aligning read pairs to reference index: ${ref_index}
mkdir aligned

for fq1 in $(find . -name '*R1*.fastq.gz'); do
  fq2=${fq1/R1/R2}
  bam=${fq1/R1_/}
  bam=${bam%%.fastq.gz}'.bam'
  bam=${bam##*/}
  echo $fq1
  echo $fq2
  echo $bam
  bwa mem -t $threads -R "@RG\tID:$runid\tSM:${bam%.bam}" $ref_index $fq1 $fq2 | samtools sort -@ $threads -O BAM > aligned/$bam
done
