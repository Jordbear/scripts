#!/bin/bash
mkdir coverage
ref=/Users/jordanbrown/sequencing/reference_genomes/mm9/mm9-new_spike/mm9-new_spike.fa
annotation=/Users/jordanbrown/sequencing/reference_genomes/spikes/synthetic_N5mCNN.bed
interval=synthetic_N5mCNN
files=(*.bam)

java -jar $PICARD BedToIntervalList \
I=$annotation \
O=coverage/interval_list-$interval.tsv \
SD=${files[0]}

for bam in *bam; do
  echo $bam
  echo $interval
  echo $ref
  java -jar $PICARD CollectWgsMetrics \
  I=$bam \
  O=coverage/${bam%%.bam}"_wgs-$interval.tsv" \
  R=$ref \
  INTERVALS=coverage/interval_list-$interval.tsv \
  COVERAGE_CAP=100000
done
