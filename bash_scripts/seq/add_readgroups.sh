#!/bin/bash
mkdir rg
for bam in .bam; do
  echo $bam
  java -jar $PICARD AddOrReplaceReadGroups \
  I=$bam \
  O=rg/${bam%.bam}_rg.bam \
  RGID=003 \
  RGLB=lib \
  RGPL=illumina \
  RGPU=unknown \
  RGSM=sample
done
