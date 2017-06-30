#!/bin/bash

name=()

for (( i = 29; i <= 52; i++)) ;
do
	name+=("S"$i)
	#echo $i

done

#echo  "array"

for i in "${name[@]}"
do
	#echo $i
	sickle pe -f *${i}*R1*.fastq -r *${i}*R2*fastq -t illumina -g -o trimmed_R1_${i}.fastq.gz \
-p trimmed_R2_${i}.fastq.gz -s trimmed_single_${i}.fastq.gz 

done
