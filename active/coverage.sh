#!/bin/bash
annotation=/Users/jordanbrown/sequencing/references/spikes/J02459.1.bed
rname=J02459.1
mkdir "coverage-${rname}"
for bam in *.bam; do
  echo $bam
  bedtools coverage -a $annotation -b $bam -d -split > coverage-${rname}/${bam%%.bam}'_coverage.tsv'
done
