#!/bin/bash
trim=$1
adapters=$2
ref_index=$3
ref=$4
annotation=$5

if [[ $trim == "true" ]]; then
  echo Trimming with adapters: $adapters
fi
echo Aligning to: $ref_index
echo Reference: $ref
echo Annotation: $annotation
echo ''



if [[ $trim == "true" ]]; then
  mkdir trimmed
  for fq1 in *1.fastq.gz; do
    fq2=${fq1%%1.fastq.gz}'2.fastq.gz'
    echo $fq1
    echo $fq2
    java -jar $TRIMMOMATIC PE -threads 4 -phred33 $fq1 $fq2 \
    trimmed/${fq1%%1.fastq.gz}'trimmed_1.fastq.gz' trimmed/${fq1%%1.fastq.gz}'trimmed_1U.fastq.gz' trimmed/${fq2%%2.fastq.gz}'trimmed_2.fastq.gz' trimmed/${fq2%%2.fastq.gz}'trimmed_2U.fastq.gz' \
    ILLUMINACLIP:${TRIMMOMATIC%%trimmomatic-0.39.jar}adapters/${adapters}:2:30:10:1:true LEADING:30 TRAILING:30 MINLEN:30
  done
  cd trimmed
fi



mkdir bams
for fq1 in *1.fastq.gz; do
  fq2=${fq1%%1.fastq.gz}'2.fastq.gz'
  echo $fq1
  echo $fq2
  echo ${fq1%%_1.fastq.gz}'.bam'
  bowtie2 -q -p 4 -X 1500 -x $ref_index -1 $fq1 -2 $fq2 | samtools sort -O BAM > bams/${fq1%%_1.fastq.gz}'.bam'
done
cd bams


mkdir dmarked
mkdir dmarked/qc
for bam in *.bam; do
  echo $bam
  java -jar $PICARD MarkDuplicates \
  I=$bam \
  O=dmarked/${bam%%.bam}'_dmarked.bam' \
  M=dmarked/qc/${bam%%.bam}'_dups.tsv'
done
cd dmarked


files=(*.bam)

for bam in *.bam; do
  echo $bam
  java -jar $PICARD CollectAlignmentSummaryMetrics \
  R=$ref \
  I=$bam \
  O=qc/${bam%%.bam}'_alignment.tsv'
done

for bam in *.bam; do
  echo $bam
  java -jar $PICARD CollectInsertSizeMetrics \
  I=$bam \
  O=qc/${bam%%.bam}'_inserts.tsv' \
  H=qc/${bam%%.bam}'_inserts.pdf'
done

for bam in *.bam; do
  echo $bam
  java -jar $PICARD CollectGcBiasMetrics \
  I=$bam \
  O=qc/${bam%%.bam}'_gc.tsv' \
  CHART=qc/${bam%%.bam}'_gc.pdf' \
  S=qc/${bam%%.bam}'_gcsummary.tsv' \
  R=$ref
done

java -jar $PICARD BedToIntervalList \
I=$annotation \
O=qc/interval_list.tsv \
SD=${files[0]}
for bam in *bam; do
  echo $bam
  java -jar $PICARD CollectTargetedPcrMetrics \
  I=$bam \
  O=qc/${bam%%.bam}'_tas.tsv' \
  R=$ref \
  AMPLICON_INTERVALS=qc/interval_list.tsv \
  TARGET_INTERVALS=qc/interval_list.tsv
done

mkdir targets
samtools view -H ${files[0]} | grep @SQ | sed 's/@SQ\tSN:\|LN://g' > targets/sort_order.tsv
for bam in *.bam; do
  echo $bam
  bedtools coverage -a $annotation -b $bam -sorted -g targets/sort_order.tsv -mean > targets/${bam%%.bam}'_targets.tsv'
done
cd qc



directory=$(which jbscripts)_dir/
${directory}alignment.py
${directory}duplication.py
${directory}gc_bias.py
${directory}insert_size.py
