#!/bin/bash
mkdir clipo
for bam in *.bam; do
  echo $bam
  bam clipOverlap --in $bam --out clipo/${bam%.bam}'_clipo.bam'
done
