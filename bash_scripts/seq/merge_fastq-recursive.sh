#!/bin/bash
mkdir merged
for fql1 in $(find . -name "*_L001_*.f???q.gz"); do
  echo $fql1
  fql1f=${fql1##*/}
  echo $fql1f
  echo ${fql1f%%_L001_*}'      '${fql1f##*_L001_}
  fqs=`find . -name "${fql1f%%_L001_*}*${fql1f##*_L001_}" -print | sort`
  fqs=${fqs//.\// }
  echo $fqs
  cat $fqs > merged/${fql1f%%_L001_*}'_'${fql1f##*_L001_}
done
