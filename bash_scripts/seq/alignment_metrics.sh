#!/bin/bash

mkdir qc

ref=/Users/jordanbrown/sequencing/reference_genomes/spikes/new_spike.fa

for bam in *.bam; do
  echo $bam
  java -jar $PICARD CollectAlignmentSummaryMetrics \
  R=$ref \
  I=$bam \
  O=qc/${bam%%.bam}'_alignment.tsv' \
  USE_JDK_DEFLATER=true \
  USE_JDK_INFLATER=true
done
