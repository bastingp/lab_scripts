#!/bin/bash
#Author: Preston Basting
#Last Changed: 4/14/2017 by PB

#This script is designed to be an easy to use method for performing all of the steps involved
#in running breseq, including subtraction of ancestral mutations and the generation of a mutation chart.

#it checks to make sure the input matches a subdirectory
#if no matches it asks again

#gets all sub_directory names and adds them to an array
name_array=()
for dir in */ ; do
	dir_name=${dir::-1}
	if [ "$dir" != "genbank" ]
	then
		name_array+=("$dir_name")
	fi
done

x=0
y=0
z=${#name_array[@]}

WT_name=$1


y=0
while [ $y -lt  $z ]; do
	if [ "$WT_name" = "${name_array[$y]}" ]
	then
		((x++))
	fi
	((y++))
done
if [ $x -lt 1 ]
then
  echo ERROR: wildtpye directory not found
  echo EXITING PROGRAM
  exit 0
fi


#mkdir gd_files
if [ ! -d gd_files ]; then
	mkdir gd_files
fi


for isolate in */ ; do
	if [ "$isolate" != "genbank/" ] && [ "$isolate" != "gd_files/" ]
	then
		iso_name=${isolate::-1} #removes '/' from end of isolate string

		#breseq called#
		breseq -j 50 -r genbank/reference/*.gb "$isolate"*R1*.fastq "$isolate"*R2*fastq -o "$isolate"

		#moves and renames .gd files#
		cp "$isolate"output/output.gd gd_files/
		#mv gd_files/output.gd gd_files/"$iso_name".gd

		#renames .bam, .bam.bai, .gff3, and .fasta
		#this makes it easier to know which files to open in IGV
	  mv "$isolate"data/reference.bam "$isolate"data/"$iso_name".bam
		  mv "$isolate"data/reference.bam.bai "$isolate"data/"$iso_name".bam.bai
		mv "$isolate"data/reference.gff3 "$isolate"data/"$iso_name".gff3
		mv "$isolate"data/reference.fasta "$isolate"data/"$iso_name".fasta

		if [ "$iso_name" = "$WT_name" ] #renames .gd of wildtype to generic WT.gd for subtraction/mutation chart
		then
			iso_name="WT"
		fi

		mv gd_files/output.gd gd_files/"$iso_name".gd
	fi
done


if [ ! -d gd_sub ]; then
	mkdir gd_sub
fi

#subtracts WT mutations from the other strains
for gd in gd_files/*.gd ; do
	if [ "$gd" != "gd_files/WT.gd" ]
		then
			gd_name=${gd#"gd_files/"}
			gd_name=${gd_name%".gd"}

			gdtools SUBTRACT -o gd_sub/"$gd_name"_sub.gd gd_files/"$gd_name".gd gd_files/WT.gd
	fi
done

gd_combined=""
for gd in gd_sub/*_sub.gd ; do
	gd_combined="${gd_combined}${gd} "
done

gdtools ANNOTATE -o mutation_chart.html -r genbank/reference_anno/*.gb ${gd_combined}
