#!/bin/bash

grep .sra .
# length=`cat $1 | wc -l`
# echo 'Detected list of legth:' $length
#
# count=1
# while [ $count -le $length ]; do
#   accession=`sed -n ${count}'p' $1`
#   echo 'Downloading accession:' $accession
#   #fastq-dump -e 6 --split-files $accession
#   ((count+=1))
# done
