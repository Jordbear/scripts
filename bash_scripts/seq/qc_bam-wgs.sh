#!/bin/bash
mkdir qc

ref=/Users/jordanbrown/sequencing/reference_genomes/spikes/new_spike-J02459.1.fa


for bam in *.bam; do
  echo $bam
  java -jar $PICARD CollectAlignmentSummaryMetrics \
  R=$ref \
  I=$bam \
  O=qc/${bam%%.bam}'_alignment.tsv' \
  USE_JDK_DEFLATER=true \
  USE_JDK_INFLATER=true
done

for bam in *.bam; do
  echo $bam
  java -jar $PICARD CollectInsertSizeMetrics \
  I=$bam \
  O=qc/${bam%%.bam}'_inserts.tsv' \
  H=qc/${bam%%.bam}'_inserts.pdf' \
  USE_JDK_DEFLATER=true \
  USE_JDK_INFLATER=true
done

for bam in *.bam; do
  echo $bam
  java -jar $PICARD CollectGcBiasMetrics \
  I=$bam \
  O=qc/${bam%%.bam}'_gc.tsv' \
  CHART=qc/${bam%%.bam}'_gc.pdf' \
  S=qc/${bam%%.bam}'_gcsummary.tsv' \
  R=$ref \
  USE_JDK_DEFLATER=true \
  USE_JDK_INFLATER=true
done

for bam in *bam; do
  echo $bam
  java -jar $PICARD CollectWgsMetrics \
  I=$bam \
  O=qc/${bam%%.bam}'_wgs.tsv' \
  R=$ref \
  USE_JDK_DEFLATER=true \
  USE_JDK_INFLATER=true
done
