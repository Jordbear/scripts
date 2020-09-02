#!/bin/bash
ref=/Users/jordanbrown/sequencing/reference_genomes/mm9/mm9-new_spike/mm9-new_spike.fa
annotation=/Users/jordanbrown/sequencing/reference_genomes/spikes/synthetic_N5mCNN.bed
interval=synthetic_N5mCNN
files=(*.bam)
mkdir artifacts

java -jar $PICARD BedToIntervalList \
I=$annotation \
O=artifacts/interval_list-$interval.tsv \
SD=${files[0]}

for bam in *bam; do
  echo $bam
  echo $interval
  echo $ref
  java -jar $PICARD CollectSequencingArtifactMetrics \
  I=$bam \
  O=artifacts/${bam%%.bam}"_artifacts-$interval.tsv" \
  R=$ref \
  INTERVALS=artifacts/interval_list-$interval.tsv
done
