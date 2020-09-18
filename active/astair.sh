#!/bin/bash
ref=/Users/jordanbrown/sequencing/references/spikes/J02459.1.fa
rname=J02459.1
mkdir "astair-${rname}"
for i in *.bam; do
  echo $i
  astair call -i $i -f $ref -d "astair-${rname}/" -md 10000 --minimum_base_quality 13 &
  ntasks=`jobs -p | wc -w`
  echo $ntasks
  if [ $ntasks -ge 3 ]; then wait; fi
done
