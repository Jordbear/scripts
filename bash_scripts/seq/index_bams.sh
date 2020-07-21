for i in *.bam; do
  samtools index $i
done
