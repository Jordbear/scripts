#!/bin/bash
mkdir astair_160mer
script=~/sequencing/160mer-ncnn-and-highly-covered-short/separator.py
for i in *.bam; do
  echo $i
  python3 $script -i $i --read_length 151 --modified_positions 51,111 --modified_positions_orientation OT,OB -d "astair_160mer/"
done
