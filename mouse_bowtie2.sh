#!/bin/bash

name=()

for (( i = 29; i <= 52; i++)) ;
do
	name+=("S"$i)
	#echo $i

done

bowtie2-build reference.fasta CARD  ##Rename reference##

mkdir readCounts
mkdir samFiles

for i in "${name[@]}"
do
	#Align reads#
	bowtie2 --local -p 56 -x CARD -1 trimmed_R1_${i}.fastq.gz -2 trimmed_R2_${i}.fastq.gz -S samFiles/${i}.sam

	#convert sam to bam#
	samtools view -bS samFiles/${i}.sam > samFiles/${i}.bam

	#sort bam file#
	samtools sort samFiles/${i}.bam samFiles/${i}.sorted.bam

	#index bam file#(Optional)
	samtools index samFiles/${i}.sorted.bam

	#write count data to csv#
	samtools idxstats samFiles/${i}.sorted.bam > readCounts/${i}_readCounts.csv
done
