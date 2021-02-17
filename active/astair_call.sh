#!/bin/bash
ref=/pipeline/references/lambda/J02459.1.fa
nthreads=`nproc --all`
mkdir astair
for i in *.bam; do
  echo $i
  astair call -i $i -f $ref -d astair -md 10000 -zc --minimum_base_quality 13 &
  ntasks=`jobs -p | wc -w`
  echo $ntasks
  if [ $ntasks -ge $nthreads ]; then wait; fi
done
