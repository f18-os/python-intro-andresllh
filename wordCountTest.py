#! /usr/bin/env python3

import sys        # command line arguments
import re         # regular expression tools
import os         # checking if file exists
import subprocess # executing program

# set input and output files
if len(sys.argv) is not 4:
    print("Correct usage: wordCountTest.py <input text file> <output file> <solution key file>")
    exit()

textFname = sys.argv[1]
outputFname = sys.argv[2]
inputFname = sys.argv[3]

#first check to make sure program exists
if not os.path.exists("wordCount.py"):
    print ("wordCount.py doesn't exist! Exiting")
    exit()

#make sure text files exist
if not os.path.exists(textFname):
    print ("text file input %s doesn't exist! Exiting" % textFname)
    exit()
    
#execute the program with 
subprocess.call(["python3", "./wordCount.py", textFname, outputFname])

#make sure output file exists
if not os.path.exists(outputFname):
    print ("wordCount output file %s doesn't exist! Exiting" % outputFname)
    exit()

    
#stats
passed = True
faults = 0
words  = 0

#master dictionary
master = {}
#dictionary to test
test = {}

# attempt to open input file
with open(inputFname, 'r') as inputFile:
    for line in inputFile:
        # get rid of newline characters
        line = line.strip()
        # split line on whitespace and punctuation
        word = re.split('[ \t]', line)
        if len(word) != 2:
            print ("Badly formatted line, exiting. Bad line:\n %s" % line)
            exit()
        master[word[0]] = int(word[1])
        words += 1

with open(outputFname, 'r') as outputFile:
    lastWord = ""
    for line in outputFile:
        # get rid of newline characters
        line = line.strip()
        # split line on whitespace and punctuation
        word = re.split('[ \t]', line)
        if len(word) != 2:
            print ("Badly formatted line, exiting. Bad line:\n %s" % line)
            exit()
        if word[0] <= lastWord:
            print ("Misordered words: %s appears before %s" % (lastWord, word[0]))
            passed = False
            faults += 1
        test[word[0]] = int(word[1])
        lastWord = word[0]
        
# see if test is missing words from master
for key in master:
    if key not in test:
        print ("Missing word in test file: %s" % key)
        passed = False
        faults += 1

# see if test has words master doesn't have
for key in test:
    if key not in master:
        print ("Extra word in test file: %s" % key)
        passed = False
        faults += 1
        
# see if counts match        
for key in master:
    if key in test and test[key] != master[key]:
        print ("Count mismatch for %s, should be %s value is %s" % (key, master[key], test[key]))
        passed = False
        faults += 1
if passed:
    print ("Passed!")
else:
    print ("Error rate {0:.3f}%".format(faults * 100.0 / words))
    print ("Failed!")
        
