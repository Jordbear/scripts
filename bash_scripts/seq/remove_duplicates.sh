#!/bin/bash
mkdir rd

for bam in *.bam; do
  echo $bam
  java -jar /mnt/e/picard.jar MarkDuplicates \
  I=$bam \
  O=rd/${bam%%.bam}'_rd.bam' \
  M=rd/qc/${bam%%.bam}'_dups.tsv' \
  REMOVE_DUPLICATES=true \
  USE_JDK_DEFLATER=true \
  USE_JDK_INFLATER=true
done
