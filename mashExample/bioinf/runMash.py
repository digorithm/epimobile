# -*- coding: utf-8 -*-
import argparse
import os
import shlex
import subprocess
import re

parser = argparse.ArgumentParser(description="Running Mash")
parser.add_argument('-inFile',required=True,type=str,help="fastq input file")
parser.add_argument('-refDB',required=True,type=str,help="RefSeqSketch location")
parser.add_argument('-outdir',type=str,help="Output directory for files")
parser.add_argument('-hashmatch',type=int,default=10,help="Hash match threshold")

args = parser.parse_args()

#preparing sketch
cmd = 'mash sketch -m 2 -k 16 -s 400 %s' % (args.inFile)
#print cmd
out= subprocess.check_output(cmd,shell=True)

#run against refseq
#mash dist ./data/RefSeqSketches.msh ./data/genome1.fna > distances2.tab
cmd = 'mash dist %s %s.msh > ./output/%s_distances.tab' % (args.refDB, args.inFile, os.path.basename(args.inFile))
#print cmd

out= subprocess.check_output(cmd,shell=True)


#sort the best results, keep all to the statistically significant ones
#
#it's not ideal to print ot a file, but the capture of stdout from MASH isn't working well, the line gets all messed up when read.

cmd = 'sort -gk3 ./output/%s_distances.tab > ./output/%s_distancesSorted.tab ' % (os.path.basename(args.inFile),os.path.basename(args.inFile))
#print cmd
out = subprocess.check_output(cmd,shell=True)

#MASH Output
#Reference-ID, Query-ID, Mash-distance, P-value, and Matching-hashes
fileID = './output/%s_distancesSorted.tab' % os.path.basename(args.inFile)
fileIN = open(fileID,'r')

# only consult first 10 lines of the sorted file, there could be hits beyond that..
# but right now, this could be could for efficiency
lines = [line for line in fileIN][:10] #

#exploring option to print some other output
results = [] #store the results

#a forloop is overkill for just selecting the first line, but I am leaving it in
# Note to self, what could also work a limit of 1 or 2 for min dist
for item in lines:
    tmp = item.split('\t')
    firstLine = False
    # so we can select top choices either by p-value or some number of hits
    # in the hash table. I am going to try that at least 10 hashes have to Matching-hashe
    # simple rule, can add confidence rating as well

    #p-value based rule (uncomment to enforce)
    #ruleVal = float(tmp[3]) < 0.0000001

    #a hit rate rule (uncomment to enforce)
    #(num,deom) = tmp[4].split("/")
    #ruleVal =  int(num) > args.hashmatch #p-value based rule

    # a grab the first line only rule (comment out both lines and change to different rule)
    ruleVal = True
    firstLine = True

    if ruleVal:
        #this captures most of them
        res = None

        outVal=re.search('\\.[0-9]?\\-[0-9]?([A-Z,a-z].*).fna',tmp[0])
        if outVal is None:
            res = tmp[0]
        else:
            res = outVal.group(1)
        results.append(res)

    if firstLine:
        break

fileIN.close()


fileID = './output/%s_orga.txt' % os.path.basename(args.inFile)
fileOUT = open(fileID,'w')

if len(results) > 0:
    for res in results:
        resultString = "%s : %s (of %d total hits)\n" % (os.path.basename(args.inFile), res, len(results))
        fileOUT.write(resultString)
else:
        resultString = "%s : No matches to current database\n" % os.path.basename(args.inFile)
        fileOUT.write(resultString)

fileOUT.close()
