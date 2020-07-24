#!/bin/bash
ref=/Users/jordanbrown/sequencing/reference_genomes/spikes/unmodified_2kb.fa
rname=unmodified_2kb
mkdir "astair-${rname}"
for i in *.bam; do
  echo $i
  astair call -i $i -f $ref -d "astair-${rname}/" -md 10000
done
