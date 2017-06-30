#!/usr/bin/python
#This script is used to take the information from two genbank files
###and create a table of locus tags and gene names

#This is useful because newer genbanks don't contain old gene names
###which makes legible gene annotation difficult


#This script generates a gene table with three columns
##Position, Locus tag from new genbank, and gene name from old genbank file
# Requires three arguments:
	## old genbank file, new genbank file and output file (.csv)
	##locus tags are parsed from new genbank
	##gene names are parsed from old genbank

#WRITTEN BY: Preston Basting
#EMAIL: bastingp@kenyon.edu
#LAST CHANGED: 5/15/2017


#### FUNCTIONS  ####

#Input: line containing start position
###Parses and returns start position
def getStartPos(line):
	start=""
	pos = line.find("gene")
	pos+= 16 #moves up to start position
	if line[pos] == 'c': #some start positions start with 'complement'
		pos+=11
	while line[pos] != '.': #'...' seperates start and end position
		if line[pos] != '<': #some start positions begin with '<'
			start+=line[pos]
		pos+=1
	return start

#Input: newest genbank file after finding start position
###Parses and returns the locus tag if there is one
def getLocusTag(file):
	locusTag = ""
	temp = ""
	for x in range(0,3): # stores next three lines
		temp+=file.readline()
	pos = temp.find("/locus_tag=")
	if pos == -1:
		locusTag = "NO_LOCUS_TAG"
		return locusTag
	else:
		pos+=12
		for y in range(pos, (pos+11)):
			locusTag+=temp[y]
		return locusTag


#INPUT: 2014 genbank file after finding start position
###Parses and returns the gene name at this start position
def getGeneName(file):
	geneName = ""
	temp = ""
	for x in range(0,3): #stores next three lines
		temp+=file.readline()
	pos = temp.find("/gene")
	if pos == -1: #if gene isn't found
		locusTag = "NO_GENE_NAME"
		return geneName
	else:
		pos+=7 #moves to gene name position
		for y in range(pos, (pos+4)):
			if temp[y] != '"':
				geneName+=temp[y]
		return geneName

#INPUT: file name of new genbank, dictionary to store locus tags
## adds start positions and locus tags to the dictionary
def addLocusTagsToDictionary(fileName, dictionary):
	if os.path.exists(fileName): #checks if given file exists
		genBank2016 = open(fileName,"r")
		line="...."
		start=""
		locusTag =""
		while line != "": #runs until end of file
			line = genBank2016.readline()
			if line.find("  gene  ") != -1: #moves to next gene
				start = getStartPos(line)
				locusTag = getLocusTag(genBank2016)
				dictionary[start].append(locusTag) #adds position and tag
	else:										   #to dictionary
		print "ERROR: new genbank file:'"+fileName+"' not found!"

#INPUT: file name of old genbank, dictionary to store gene names
##adds start positions(if they are new) and gene names to dictionary
def addGeneNamesToDictionary(fileName, dictionary):
	if os.path.exists(fileName):#checks if file exists
		genBank2014 = open(fileName,"r")
		line="..."
		start=""
		geneName=""
		while line != "":
			line = genBank2014.readline()
			if line.find("  gene  ") != -1: #moves to next gene
				start = getStartPos(line)
				geneName = getGeneName(genBank2014)
				if len(dictionary[start]) ==0:
					dictionary[start].append("NONE") #adds a blank value if-
				dictionary[start].append(geneName) #-no locus tag exists
	else:
		print "ERROR: old genbank file:'"+fileName+"' not found!"


#INPUT: output file name and dictionary of gene positions, locus tags and gene names
def writeDictToFile(fileName, dictionary):
	file = open(fileName, "w") #creates file if it doesn't exist
	name = ""
	for startPos in dictionary: #loops through positions
		file.write(startPos)
		file.write(",")
		if len(dictionary[startPos]) == 1:
			dictionary[startPos].append("NONE")
		for name in dictionary[startPos]: #loops through locus tags and gene names
			file.write(name)
			file.write(",")
		file.write("\n")


#####  MAIN  #######
import sys #needed to get arguments
oldGenBank = sys.argv[1] #argument 1
newGenBank = sys.argv[2] #argument 2
oututFileName = sys.argv[3] #argument 3

from collections import defaultdict
geneDict = defaultdict(list) #Initializes dictionary of lists

import os.path #needed to tell if files exist
addLocusTagsToDictionary(newGenBank, geneDict)
addGeneNamesToDictionary(oldGenBank, geneDict)
writeDictToFile(oututFileName, geneDict)
print "done!"