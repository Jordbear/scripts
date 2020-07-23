#!/bin/bash
reads=()

for i in *.bam; do
  r=$(samtools view -c -@ 6 $i)
  echo $i
  echo $r
  reads+=($r)
done

echo ${reads[@]}

min=${reads[0]}
for i in ${reads[@]}; do
  if (($i<$min)); then
    min=$i
  fi
done

echo $min

dprop=()

for i in ${reads[@]}; do
  d=$(echo print $min/$i | perl)
  echo $d
  dprop+=($d)
done

echo ${dprop[@]}

mkdir downsampled
count=0
for i in *.bam; do
  echo $i
  echo ${dprop[$count]}
  java -jar $PICARD DownsampleSam I=$i O=downsampled/${i%%.bam}'_ds.bam' PROBABILITY=${dprop[$count]} USE_JDK_DEFLATER=true USE_JDK_INFLATER=true
  count=$((count+1))
done
