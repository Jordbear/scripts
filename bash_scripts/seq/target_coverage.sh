#!/bin/bash
mkdir targets
genes=/mnt/e/ref_human/hg19/CancerHotSpot-v2.dna_manifest.20180509_nuc.bed

for bam in *.bam; do
  echo $bam
  bedtools coverage -a $genes -b $bam -mean > targets/${bam%%.bam}'_targets.tsv'
done
