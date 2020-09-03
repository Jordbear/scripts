#!/bin/bash
ref=/data/references/mm10-base_spikes/mm10-base_spikes.fa
annotation=/data/references/spikes/unmodified_2kb.bed
interval=unmodified_2kb

mkdir artifacts
files=(*.bam)

java -jar $PICARD BedToIntervalList \
I=$annotation \
O=artifacts/$interval.interval_list \
SD=${files[0]}

for bam in *bam; do
  echo $bam
  echo $interval
  echo $ref
  java -jar $PICARD CollectSequencingArtifactMetrics \
  I=$bam \
  O=artifacts/${bam%%.bam}"_artifacts-$interval" \
  R=$ref \
  INTERVALS=artifacts/$interval.interval_list
done
