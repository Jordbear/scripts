#!/bin/bash
adapters=TruSeq3-PE.fa
echo Trimming adapters: $adapters
ref_index=/mnt/e/ref_bacteria/T/E_coli_tfs/bowtie2_tfs/tfs
echo Aligning to: ${ref_index}
ref=/mnt/e/ref_bacteria/T/E_coli_tfs/e_coli_tfs.fasta
echo Referencing: $ref

echo ''



mkdir trimmed
for fq1 in *1.fastq.gz; do
  fq2=${fq1%%1.fastq.gz}'2.fastq.gz'
  echo $fq1
  echo $fq2
  java -jar /mnt/e/Trimmomatic-0.39/trimmomatic-0.39.jar PE -threads 4 -phred33 $fq1 $fq2 \
  trimmed/${fq1%%1.fastq.gz}'trimmed_1.fastq.gz' trimmed/${fq1%%1.fastq.gz}'trimmed_1U.fastq.gz' trimmed/${fq2%%2.fastq.gz}'trimmed_2.fastq.gz' trimmed/${fq2%%2.fastq.gz}'trimmed_2U.fastq.gz' \
  ILLUMINACLIP:/mnt/e/Trimmomatic-0.39/adapters/$adapters:2:30:10:1:true LEADING:30 TRAILING:30 MINLEN:30
done


cd trimmed
mkdir bams
echo Aligning read pairs to reference: ${ref_index}
for fq1 in *1.fastq.gz; do
  fq2=${fq1%%1.fastq.gz}'2.fastq.gz'
  echo $fq1
  echo $fq2
  echo ${fq1%%_1.fastq.gz}'.bam'
  bowtie2 -q -p 4 -X 1500 -x $ref_index -1 $fq1 -2 $fq2 | samtools sort -O BAM > bams/${fq1%%_1.fastq.gz}'.bam'
done


cd bams
mkdir dmarked
mkdir dmarked/qc
for bam in *.bam; do
  echo $bam
  java -jar /mnt/e/picard.jar MarkDuplicates \
  I=$bam \
  O=dmarked/${bam%%.bam}'_dmarked.bam' \
  M=dmarked/qc/${bam%%.bam}'_dups.tsv'
done


cd dmarked
for bam in *.bam; do
  echo $bam
  java -jar /mnt/e/picard.jar CollectAlignmentSummaryMetrics \
  R=$ref \
  I=$bam \
  O=qc/${bam%%.bam}'_alignment.tsv'
done

for bam in *.bam; do
  echo $bam
  java -jar /mnt/e/picard.jar CollectInsertSizeMetrics \
  I=$bam \
  O=qc/${bam%%.bam}'_inserts.tsv' \
  H=qc/${bam%%.bam}'_inserts.pdf'
done

for bam in *.bam; do
  echo $bam
  java -jar /mnt/e/picard.jar CollectGcBiasMetrics \
  I=$bam \
  O=qc/${bam%%.bam}'_gc.tsv' \
  CHART=qc/${bam%%.bam}'_gc.pdf' \
  S=qc/${bam%%.bam}'_gcsummary.tsv' \
  R=$ref
done

for bam in *bam; do
  echo $bam
  java -jar /mnt/e/picard.jar CollectWgsMetrics \
  I=$bam \
  O=qc/${bam%%.bam}'_wgs.tsv' \
  R=$ref
done



cd qc
alignment.py
duplication.py
gc_bias.py
insert_size.py
