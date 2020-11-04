#!/bin/bash
mkdir trimmed

for fq1 in $(find . -name '*R1*.fastq.gz'); do
  fq2=${fq1/R1/R2}
  fq1f=${fq1##*/}
  fq2f=${fq2##*/}
  echo $fq1
  echo $fq2
  echo ${fq1f}
  echo ${fq2f}
  trim_galore --length 35 -o trimmed --no_report_file -j 4 --paired $fq1 $fq2
done
