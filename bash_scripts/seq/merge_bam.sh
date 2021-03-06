#!/bin/bash
mkdir merged
for bam in *L001*.bam; do
  echo $bam
  echo ${bam%%_L001*}${bam##*L001}
  bams=`find . -name "${bam%%_L001*}*${bam##*L001}" -print0 | sort -z | tr -d '\000'`
  echo $bams
  input=${bams//.\// I=}
  input=${input# }
  echo $input
  java -jar $PICARD MergeSamFiles $input O=merged/${bam%%_L001*}${bam##*L001} USE_JDK_DEFLATER=true USE_JDK_INFLATER=true USE_THREADING=true
done
