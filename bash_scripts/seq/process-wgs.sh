#!/bin/bash
ref_index=/mnt/e/ref_bacteria/T/E_coli_tfs/bowtie2_tfs/tfs
ref=/mnt/e/ref_bacteria/T/E_coli_tfs/e_coli_tfs.fasta



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
  O=qc/${bam%%.bam}'_insert.tsv' \
  H=qc/${bam%%.bam}'_insert.pdf'
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
