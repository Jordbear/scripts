#!/bin/bash
ref=/Users/jordanbrown/sequencing/references/
rname=test
mkdir "astair-${rname}"
for i in *.bam; do
  echo $i
  astair call -i $i -f $ref -d "astair-${rname}/" -md 10000 &
  ntasks=`jobs -p | wc -w`
  echo $ntasks
  if [ $ntasks -ge 6 ]; then wait; fi
done
