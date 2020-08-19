#!/bin/bash
for sra_path in $(find . -name '*.sra'); do
  sra=${sra_path##*/}
  echo "Dumping $sra to fastq"
  fasterq-dump -e 6 --split-files $sra
  mv $sra'_1.fastq' ${sra%%.sra}'_1.fastq'
  mv $sra'_2.fastq' ${sra%%.sra}'_2.fastq'
  echo 'Compressing fastq files with gzip'
  pigz -p 6 ${sra%%.sra}'_1.fastq' ${sra%%.sra}'_2.fastq'
done
