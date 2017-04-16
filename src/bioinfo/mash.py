import logging
import os
import subprocess
import hashlib
from database.mash_db import MashDB
import re

class Mash(object):
  
  def __init__(self, k_mers=16, sketch_size=400, k_mer_copies=2):
    self.reference_db = None
    self.k_mers = k_mers
    self.sketch_size = sketch_size
    self.k_mer_copies = k_mer_copies
    self.mash_db = MashDB()

  def set_reference_db(self, db_path):
    """
    Set the reference database that will be used by the mash algorithm.
    Default should be in: bioinfo/data/RefSeqSketches.msh
    """
    self.reference_db = db_path

  def run_mash(self, file_path, hash_match=10):
    """
    Run mash algorithm against a DNA sample. File_path must be a path to
    a fastq.gz file. Bash match is the threshold used by the mash. 
    """
    # Preparing sketch
    cmd = 'mash sketch -m {} -k {} -s {} {}'.format(self.k_mer_copies, self.k_mers, self.sketch_size, file_path)
    out = subprocess.check_output(cmd, shell=True)
    
    # Run against refseq
    cmd = 'mash dist {} {}.msh > {}/output/{}_distances.tab'.format(self.reference_db, file_path, os.path.dirname(os.path.abspath(__file__)), os.path.basename(file_path))

    out = subprocess.check_output(cmd, shell=True)

    file_hash = hashlib.md5(file_path.encode())
    sample_id = self.mash_db.save_sample_result(file_hash.hexdigest())

    self.save_output(file_path, sample_id)
    
    top_n = self.mash_db.get_top_n_mash_results(sample_id)

    top_result = self.get_top_result(top_n)

    if len(top_result) > 0:
      print "Total hits: {}".format(len(top_result))
      print top_result

    query_arg = ', '.join(top_result)

    # Send final result for this dna sample to the database
    self.mash_db.update_sample_result(sample_id, query_arg)

  def save_output(self, file_path, sample_id):
    """
    Save mash output in database
    """
    with open("{}/output/{}_distances.tab".format(os.path.dirname(os.path.abspath(__file__)), os.path.basename(file_path)), "r") as d:
      output = d.read()
      
      # Get each row from the mash output
      output_rows = map(lambda x: x.split("\t"), output.split("\n"))
       
      # Save rows
      self.mash_db.save_mash_output(sample_id, output_rows)

  def get_top_result(self, top_n):
    """
    Get top n results from mash output given a dna sample
    """
    result = []
    for row in top_n: 
      search = re.search('\\.[0-9]?\\-[0-9]?([A-Z,a-z].*).fna',row[1])
      res = None
      if search is None:
        res = row[1]
      else:
        res = search.group(1)
      result.append(res)
    
    return result
