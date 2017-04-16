from flask import Flask, render_template, request, redirect, url_for, make_response
from os import listdir
from os.path import isfile, join, splitext, basename
import json
import time

app = Flask(__name__, template_folder='views/templates', static_folder='views/static')
fastaFilesDir = 'fasta'

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


class ResultsEntry:
    def __init__(self, ID, disease, result):
        self.id = ID # entry id
        self.disease = disease
        self.isPositive = result # boolean or null


@app.route('/dashboard')
def showDashboard():

    # query local database and retrieve the results table
    results_list_table = []
    # below is some fake data
    results_list_table.append(ResultsEntry('1423rf83252', 'ebola', False))
    results_list_table.append(ResultsEntry('h45g3263464', 'ebola', True))
    results_list_table.append(ResultsEntry('fdyhesh4645', 'ebola', True))


    # get list of names of local fasta files
    local_files = [f for f in listdir(fastaFilesDir) if isfile(join(fastaFilesDir, f))]
    local_files = [splitext(basename(f))[0] for f in local_files]


    local_files_table = []
    for file in local_files:
        for result in results_list_table:
            if file == result.id:
                local_files_table.append(ResultsEntry(result.id, result.disease, result.isPositive))
            else:
                local_files_table.append(ResultsEntry(file, 'N/A', None))
            break


    return render_template('index.html', local_files_table=[obj.__dict__ for obj in local_files_table], 
                                        results_list_table=[obj.__dict__ for obj in results_list_table])

@app.route('/analyze', methods=['POST'])
def analyze():

    _seqID = request.form['seqID']

    # reference to the bioinfo unit
    # analyze file with _seqID and redirect to the dashboard page
    return redirect(url_for('showDashboard'))


if __name__ == "__main__":
    app.run()


