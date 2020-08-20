#!/bin/bash
targets=/mnt/e/ref_human/hg19/ampliseq_CHPv2/CancerHotSpot-v2.dna_manifest.20180509.sort.nuc.bed

mkdir targets
files=(*.bam)
samtools view -H ${files[0]} | grep @SQ | sed 's/@SQ\tSN:\|LN://g' > targets/sort_order.tsv
for bam in *.bam; do
  echo $bam
  bedtools coverage -a $targets -b $bam -sorted -g targets/sort_order.tsv -mean > targets/${bam%%.bam}'_targets.tsv'
done
