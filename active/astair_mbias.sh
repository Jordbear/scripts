#!/bin/bash
ref=/Users/jordanbrown/sequencing/references/GRCh38-base_spikes_pUC19/Homo_sapiens.GRCh38.dna_sm.primary_assembly-base_spikes.fa
rname=J02459.1
mkdir "astair_mbias-${rname}"
for i in *.bam; do
  echo $i
  astair mbias -i $i -f $ref -d "astair_mbias-${rname}/" --method mCtoT --read_length 150 -chr $rname --plot &
  ntasks=`jobs -p | wc -w`
  echo $ntasks
  if [ $ntasks -ge 3 ]; then wait; fi
done
