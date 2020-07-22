#!/bin/bash
ref=/Users/jordanbrown/sequencing/reference_genomes/spikes/J02459.1.fa
mkdir astair
for i in *.bam; do
  echo $i
  astair call -i $i -f $ref -d 'astair/'
done
