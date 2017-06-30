#!/usr/bin/python

#This script takes a csv containing a column of locus tags and creates a file containing the corresponding
##gene names for the given locus tags

#This is accomplished by comparing the locus tags to the appropriate csv file made by makeGeneChart.py

#This is useful for RNAseq when a newer genbank is used as the reference as only the locus tags are given
##This removes the need to manually look up thousands of gene names to make the results comprehensible

#This script makes a csv file that contains a table with two columns:
	#Column 1: Locus Tags Given
	#Column 2: The corresponding gene name (or the locus tag again if no gene name was found)

#This script requires 3 arguments:
	#ARG 1: Input file Name (csv with one column of locus tags)
	#ARG 2: Gene Chart generated with makeGeneChart.py using the correct genbank files
	#ARG 3: The name of the output file that will contain the gene names for the given locus tags

#WRITTEN BY: Preston Basting
#EMAIL: bastingp@kenyon.edu
#LAST CHANGED: 5/17/2017

###############
#  FUNCTIONS  #
###############

#Checks to see if provided files exist
def filesExist(inputFileName, reference):
	if os.path.exists(inputFileName):
		exists = True
	else:
		print "ERROR: "+inputFileName+" not found!"
		return False
	if os.path.exists(reference):
		return exists #returns true if both exist
	else:
		print "ERROR: "+reference+" not found!"

#Takes a line with three comma delimited values
#adds each value to a list
def lineToList(line):
	newList = []
	data = ""
	if line.find(",") == -1: #checks if line is delimited
		return newList
	for i in range (0,3): #each row has three columns
		for x in range(0,len(line)):
			if line[x] != ",":
				data += line[x]
			else: #adds string to list if delimiter is reached
				data = data.rstrip('\n')
				data = data.strip()
				newList.append(data)
				data = ""
	return newList

#Takes a csv file with three columns
#makes a dictionary of strings
#Second column(locus tag) is key
#Third column (gene name) is value
def getDictFromReference(refName, dictionary):
	ref = open(refName,"r")
	name = ""
	line = " "
	while line != "": #for every line in file
		line = ref.readline()
		lineList = lineToList(line)
		if len(lineList) > 0:
			dictionary[lineList[1]] = lineList[2]

#takes a single column csv
#converts it to a list
def fileToList(file):
	tagList = []
	line = " "
	locusTag = ""
	while line != "":
		line = file.readline()
		line = line.rstrip('\n') #removes endline
		line = line.strip() #removes spaces from beg and end
		tagList.append(line)
	return tagList


#takes a list of locus tags
#uses a dictionary to make a list of corresponding gene names
def tagsToGeneNames(tagList, dictionary):
	geneList = []
	for i in range(0,len(tagList)):
		if tagList[i] in dictionary.keys():
			if dictionary[tagList[i]].find("NONE") == -1: #if a gene name is found
				geneList.append(dictionary[tagList[i]]) #add gene name to gene list
			else:
				geneList.append(tagList[i]) #otherwise add the locus tag
		else:
			geneList.append("LOCUS_NOT_FOUND") #if the locus tag wasn't in dict
	return geneList

#takes a list of locus tags and gene names, as well as an output file name
#outputs a two column csv table to the output file
def writeToFile(tags, genes, fileName):
	file = open(fileName, "w") #creates output file
	for i in range(0,len(tags)):
		file.write(tags[i]) #col 1 : locus tag
		if i != (len(tags)-1): #last tag is always blank
			file.write(",")
			file.write(genes[i]) #col 2 : gene name
			file.write("\n")

#takes a file contiaining locus tags, a dictionary of locusTags:geneNames and an output file
#parses locus tags from file, makes a list of corresponding gene names and outputs as a csv
def getNamesFromDict(inputFileName, dictionary, outputFileName):
	inputFile = open(inputFileName, "r")
	locusTags = fileToList(inputFile)
	geneNames = tagsToGeneNames(locusTags, dictionary)
	writeToFile(locusTags, geneNames, outputFileName)


############
#   MAIN   #
############

import sys #needed to get arguments
import os.path #needed to tell if files exist
inputFileName = sys.argv[1] #argument 1
reference = sys.argv[2] #argument 2
outputFileName = sys.argv[3] #argument 3


refDict = dict()

if filesExist(inputFileName, reference) != True:
	print "ERROR in argument file names"
else:
	getDictFromReference(reference, refDict)
	getNamesFromDict(inputFileName, refDict, outputFileName)
	print "Done!"
