#!/bin/bash
ref=/data/references/mm10-base_spikes/mm10-base_spikes.fa
annotation=/data/references/spikes/unmodified_2kb.bed
interval=unmodified_2kb
files=(*.bam)

mkdir artifacts
files=(*.bam)

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
