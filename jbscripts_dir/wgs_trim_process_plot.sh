#!/bin/bash
adapters=$1
ref_index=$2
ref=$3

echo Trimming adapters: $adapters
echo Aligning to: $ref_index
echo Referencing: $ref
echo ''



mkdir trimmed
for fq1 in *1.fastq.gz; do
  fq2=${fq1%%1.fastq.gz}'2.fastq.gz'
  echo $fq1
  echo $fq2
  java -jar $TRIMMOMATIC PE -threads 4 -phred33 $fq1 $fq2 \
  trimmed/${fq1%%1.fastq.gz}'trimmed_1.fastq.gz' trimmed/${fq1%%1.fastq.gz}'trimmed_1U.fastq.gz' trimmed/${fq2%%2.fastq.gz}'trimmed_2.fastq.gz' trimmed/${fq2%%2.fastq.gz}'trimmed_2U.fastq.gz' \
  ILLUMINACLIP:${TRIMMOMATIC%%trimmomatic-0.39.jar}adapters/${adapters}:2:30:10:1:true LEADING:30 TRAILING:30 MINLEN:30
done


cd trimmed
mkdir bams
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
  java -jar $PICARD MarkDuplicates \
  I=$bam \
  O=dmarked/${bam%%.bam}'_dmarked.bam' \
  M=dmarked/qc/${bam%%.bam}'_dups.tsv'
done


cd dmarked
for bam in *.bam; do
  echo $bam
  java -jar $PICARD CollectAlignmentSummaryMetrics \
  R=$ref \
  I=$bam \
  O=qc/${bam%%.bam}'_alignment.tsv'
done

for bam in *.bam; do
  echo $bam
  java -jar $PICARD CollectInsertSizeMetrics \
  I=$bam \
  O=qc/${bam%%.bam}'_inserts.tsv' \
  H=qc/${bam%%.bam}'_inserts.pdf'
done

for bam in *.bam; do
  echo $bam
  java -jar $PICARD CollectGcBiasMetrics \
  I=$bam \
  O=qc/${bam%%.bam}'_gc.tsv' \
  CHART=qc/${bam%%.bam}'_gc.pdf' \
  S=qc/${bam%%.bam}'_gcsummary.tsv' \
  R=$ref
done

for bam in *bam; do
  echo $bam
  java -jar $PICARD CollectWgsMetrics \
  I=$bam \
  O=qc/${bam%%.bam}'_wgs.tsv' \
  R=$ref
done



cd qc
directory=$(which jbscripts)_dir/
${directory}alignment.py
${directory}duplication.py
${directory}gc_bias.py
${directory}insert_size.py
