#!/bin/bash
mkdir dmarked
mkdir dmarked/qc

ref=/mnt/e/ref_human/Homo_sapiens.GRCh38.dna_sm.primary_assembly.fa

for bam in *.bam; do
  echo $bam
  java -jar /mnt/e/picard.jar MarkDuplicates \
  I=$bam \
  O=dmarked/${bam%%.bam}'_dmarked.bam' \
  M=dmarked/qc/${bam%%.bam}'_dups.tsv'
done

for bam in dmarked/*.bam; do
  echo $bam
  base=${bam##dmarked/}
  echo $base
  java -jar /mnt/e/picard.jar CollectAlignmentSummaryMetrics \
  R=$ref \
  I=$bam \
  O=dmarked/qc/${base%%.bam}'_alignment.tsv'
done

for bam in dmarked/*.bam; do
  echo $bam
  base=${bam##dmarked/}
  echo $base
  java -jar /mnt/e/picard.jar CollectInsertSizeMetrics \
  I=$bam \
  O=dmarked/qc/${base%%.bam}'_insert.tsv' \
  H=dmarked/qc/${base%%.bam}'_insert.pdf'
done

for bam in dmarked/*.bam; do
  echo $bam
  base=${bam##dmarked/}
  echo $base
  java -jar /mnt/e/picard.jar CollectRnaSeqMetrics \
  I=$bam \
  O=dmarked/qc/${base%%.bam}'_rnaseq.tsv' \
  REF_FLAT=/mnt/e/ref_human/refFlat.txt \
  STRAND=NONE \
  RIBOSOMAL_INTERVALS=/mnt/e/ref_human/Homo_sapiens.GRCh38.98.rRNA_intervals.interval_list \
  CHART_OUTPUT=dmarked/qc/${base%%.bam}'_rnaseq.pdf'
done
