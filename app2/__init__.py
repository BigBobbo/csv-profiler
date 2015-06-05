import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename
import pandas as pd
import numpy as np
from .profiler import profileGen


UPLOAD_FOLDER = '/home/csvprofiler/csv-profiler/app2/uploads'
cwd = os.getcwd()
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <h2>''' + str(cwd) + '''</h2>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''



@app.route('/uploads/<filename>')
def uploaded_file(filename):
    # x = pd.DataFrame.from_csv(app.config['UPLOAD_FOLDER'] + "/" + filename)
    # os.remove(app.config['UPLOAD_FOLDER'] + "/" + filename)
    x = profileGen(app.config['UPLOAD_FOLDER'] + "/" + filename)
    return render_template("analysis.html", name=filename, data=x.to_html())


@app.route('/analysis/<filename>')
def analysis(filename):
    x = pd.DataFrame(np.random.randn(20, 5))
    return render_template("analysis.html", name=filename, data=x.to_html())
