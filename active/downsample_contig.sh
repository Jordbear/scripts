#!/bin/bash
contig=J02459.1

samples=()
contig_reads=()
total_reads=()
ratios=()
for i in *.bam; do
  cr=$(samtools view -F 2048 -@ 6 $i | grep $contig | wc -l | bc)
  tr=$(samtools view -F 2048 -c -@ 6 $i)
  ratio=$(echo print $cr/$tr | perl)
  echo $i
  echo $cr
  echo $tr
  echo $ratio
  samples+=($i)
  contig_reads+=($cr)
  total_reads+=($tr)
  ratios+=($ratio)
done

printf "sample"$'\t' > read_totals.tsv
printf '%s\t' ${samples[@]} >> read_totals.tsv
echo $'\r' >> read_totals.tsv
printf "${contig}_reads"$'\t' >> read_totals.tsv
printf '%s\t' ${contig_reads[@]} >> read_totals.tsv
echo $'\r' >> read_totals.tsv
printf "total_reads"$'\t' >> read_totals.tsv
printf '%s\t' ${total_reads[@]} >> read_totals.tsv
echo $'\r' >> read_totals.tsv
printf "ratio"$'\t' >> read_totals.tsv
printf '%s\t' ${ratios[@]} >> read_totals.tsv

echo ${contig_reads[@]}

min=${contig_reads[0]}
for i in ${contig_reads[@]}; do
  if (($i<$min)); then
    min=$i
  fi
done

echo $min

dprop=()

for i in ${contig_reads[@]}; do
  d=$(echo print $min/$i | perl)
  echo $d
  dprop+=($d)
done

echo ${dprop[@]}

mkdir downsampled_$contig
count=0
for i in *.bam; do
  echo $i
  echo ${dprop[$count]}
  java -jar $PICARD DownsampleSam I=$i O=downsampled_$contig/${i%%.bam}'_ds.bam' PROBABILITY=${dprop[$count]} USE_JDK_DEFLATER=true USE_JDK_INFLATER=true &
  ntasks=`jobs -p | wc -w`
  echo $ntasks
  if [ $ntasks -ge 6 ]; then wait; fi
  count=$((count+1))
done
