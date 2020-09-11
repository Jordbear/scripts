#!/bin/bash
ref=/Users/jordanbrown/sequencing/references/GRCh38-base_spikes/Homo_sapiens.GRCh38.dna_sm.primary_assembly-base_spikes.fa
annotation=/Users/jordanbrown/sequencing/references/GRCh38/Homo_sapiens.GRCh38.dna_sm.primary_assembly.bed
interval=GRCh38

mkdir artifacts2
files=(*.bam)

java -jar $PICARD BedToIntervalList \
I=$annotation \
O=artifacts2/$interval.interval_list \
SD=${files[0]}

for bam in *bam; do
  echo $bam
  echo $interval
  echo $ref
  java -jar $PICARD CollectSequencingArtifactMetrics \
  I=$bam \
  O=artifacts2/${bam%%.bam}"_artifacts-$interval" \
  R=$ref \
  INTERVALS=artifacts/$interval.interval_list &
  ntasks=`jobs -p | wc -w`
  echo $ntasks
  if [ $ntasks -ge 6 ]; then wait -n; fi
done
