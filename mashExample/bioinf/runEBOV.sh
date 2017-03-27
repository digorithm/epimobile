#!/bin/sh

#to run only test files uncomment below
FILES=$(ls ../data/ebov/*.fastq.gz | head -n 16)

#FILES=$(ls ../data/ebov/*.fastq.gz)

for filename in $FILES
do
  echo $filename
  python runMash.py -inFile=$filename -refDB ../data/RefSeqSketches.msh -hashmatch 10
done

cat ./output/*orga.txt > allResults.txt
