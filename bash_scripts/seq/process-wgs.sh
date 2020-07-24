#!/bin/bash
ref_index=/Users/jordanbrown/sequencing/reference_genomes/spikes/bowtie2_index/spikes
echo Aligning to: ${ref_index}
ref=/Users/jordanbrown/sequencing/reference_genomes/spikes/new_spike.fa
echo Referencing: $ref

echo ''



mkdir bams
echo Aligning read pairs to reference: ${ref_index}
for fq1 in *R1*.fastq.gz; do
  fq2=${fq1/R1/R2}
  bam=${fq1/R1_/}
  bam=${bam%%.fastq.gz}'.bam'
  echo $fq1
  echo $fq2
  echo $bam
  bowtie2 -q -p 6 -X 1000 -x $ref_index -1 $fq1 -2 $fq2 | samtools sort -@ 6 -O BAM > bams/$bam
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

for bam in *bam; do
  echo $bam
  java -jar $PICARD CollectWgsMetrics \
  I=$bam \
  O=qc/${bam%%.bam}'_wgs.tsv' \
  R=$ref
done
