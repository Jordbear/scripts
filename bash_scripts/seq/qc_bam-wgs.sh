#!/bin/bash
mkdir dmarked
mkdir dmarked/qc

ref=/mnt/e/ref_bacteria/T/E_coli_tfs/e_coli_tfs.fasta

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
  java -jar /mnt/e/picard.jar CollectGcBiasMetrics \
  I=$bam \
  O=dmarked/qc/${base%%.bam}'_gc.tsv' \
  CHART=dmarked/qc/${base%%.bam}'_gc.pdf' \
  S=dmarked/qc/${base%%.bam}'_gcsummary.tsv' \
  R=$ref
done

for bam in dmarked/*bam; do
  echo $bam
  base=${bam##dmarked/}
  echo $base
  java -jar /mnt/e/picard.jar CollectWgsMetrics \
  I=$bam \
  O=dmarked/qc/${base%%.bam}'_wgs.tsv' \
  R=$ref
done
