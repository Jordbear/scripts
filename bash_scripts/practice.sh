#!/bin/bash
reads=()

for i in test*; do
  r=$(grep C $i | awk '{print $2}')
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

count=0
for i in test*; do
  echo ${dprop[$count]}
  count=$((count+1))
done
