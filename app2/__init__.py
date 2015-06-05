import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, request
from werkzeug import secure_filename
import pandas as pd
import numpy as np
from .profiler import profileGen
import shutil

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
            ip_dir = os.path.join(app.config['UPLOAD_FOLDER'], request.headers['X-Real-IP'].replace(".", ""))
            os.mkdir(ip_dir)
            filename = secure_filename(file.filename)
            file.save(os.path.join(ip_dir, filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return render_template("upload.html")



@app.route('/uploads/<filename>')
def uploaded_file(filename):
    ip_dir = os.path.join(app.config['UPLOAD_FOLDER'], request.headers['X-Real-IP'].replace(".", ""))
    x = profileGen(ip_dir + "/" + filename)
    shutil.rmtree(ip_dir)
    # x = profileGen(app.config['UPLOAD_FOLDER'] + "/" + filename)
    # os.remove(app.config['UPLOAD_FOLDER'] + "/" + filename)
    return render_template("analysis.html", name=filename, data=x.to_html())


@app.route('/analysis/<filename>')
def analysis(filename):
    x = pd.DataFrame(np.random.randn(20, 5))
    return render_template("analysis.html", name=request.headers['X-Real-IP'], data=x.to_html())
