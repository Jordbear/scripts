#!/bin/bash
annotation=/Users/jordanbrown/sequencing/reference_genomes/spikes/J02459.1.bed
mkdir coverage
for bam in *.bam; do
  echo $bam
  bedtools coverage -a $annotation -b $bam -hist > coverage/${bam%%.bam}'_coverage.tsv'
done
