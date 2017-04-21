from flask import Flask, render_template, request, redirect, url_for, make_response
from os import listdir
from os.path import isfile, join, splitext, basename
import json
import time
import hashlib
from database.mash_db import MashDB
from bioinfo.mash import Mash

class ResultsEntry:
    def __init__(self, ID, highest_hits, wasAnalyzed):
        self.id = ID # entry id
        self.highest_hits = highest_hits
        self.wasAnalyzed = wasAnalyzed


app = Flask(__name__, template_folder='views/templates', static_folder='views/static')
fastaFilesDir = 'src/bioinfo/data/ebov/'

mdb = MashDB()

# TODO: 3 or greater out of 400, include in results, otherwise no hits
# TODO: Fix path things, make sure it's working

@app.route('/')
def main():
    return redirect(url_for('signIn'))

@app.route('/signIn')
def signIn():
    return render_template('signin.html')

@app.route('/validateSignIn', methods=['POST'])
def validateSignIn():
    _userName = request.form['userName']
    _password = request.form['inputPassword']
    
    # validate the received values
    if _userName=='test' and _password=='test':
        return redirect(url_for('showDashboard'))
    else:
        return 'Wrong credentials. Try again.'

@app.route('/dashboard')
def showDashboard():

    # get list of names of local fasta files
    local_files = [f for f in listdir(fastaFilesDir) if isfile(join(fastaFilesDir, f))]

    # Get only the .gz files    
    zipped_files = []
    for idx, file in enumerate(local_files):
        if file.split(".")[-1] == "gz":
            zipped_files.append(file)
    
    local_files_table = []
    for file in zipped_files:
        file_hash = hashlib.md5(file.encode()).hexdigest()
        result = mdb.get_sample_by_id(file_hash)
        if len(result) != 0:
            highest_hits = result[0][2].split(",")
            local_files_table.append(ResultsEntry(file, highest_hits[0], True))
        else:
            local_files_table.append(ResultsEntry(file, 'N/A', False))

    return render_template('index.html', local_files_table=[obj.__dict__ for obj in local_files_table])

@app.route('/analyze', methods=['POST'])
def analyze():

    _seqID = request.form['seqID']

    mash = Mash()

    mash.set_reference_db("src/bioinfo/data/RefSeqSketches.msh")

    mash.run_mash(join(fastaFilesDir, _seqID))

    return redirect(url_for('showDashboard'))


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')


