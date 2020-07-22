#!/bin/bash
ref=/Users/jordanbrown/sequencing/reference_genomes/spikes/synthetic_N5mCNN.fa
rname=synthetic_N5mCNN
mkdir "astair-${rname}"
for i in *.bam; do
  echo $i
  astair call -i $i -f $ref -d "astair-${rname}/"
done
