from flask import render_template, request
from werkzeug import secure_filename
from app import app
from threading import Thread
import zipfile
import os
from datetime import datetime
import webbrowser


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route('/results')
@app.route('/results/<list_of_names>')
def results(list_of_names=None):
    return render_template("results.html", list_of_names=list_of_names)

# @app.route('/upload')
# def upload_file():
#     return render_template('index.html')


@app.route('/conversation/<id>/<now>')  # /landingpageA
def conversation(id, now):
    t = Thread(target=file_checker, args=(id,now,))
    t.start()
    return render_template("waiting_room.html")


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        now = datetime.now().time()
        os.mkdir('generated_conversations/' + str(now))
        path = 'generated_conversations/' + str(now) + '/' + secure_filename(f.filename)

        f.save(path)
        with zipfile.ZipFile(path, 'r') as zip_ref:
            zip_ref.extractall('generated_conversations/' + str(now) + '/')
        os.remove(path)
        list_of_names = os.listdir('generated_conversations/' + str(now) + '/messages/inbox')
        list_of_names.append(now)

        return render_template('results.html', list_of_names=list_of_names)


def file_checker(filename='ahoj', now='none'):
    os.system('./fb2tex -output ' + str(filename) + ' -convo "' + str(filename) + '" -root generated_conversations/' + str(now))
    path = 'out/' + filename + '.html'

    return webbrowser.open_new_tab('file:////Users/kvasntom/Google%20Drive/computers/programming/go_workspace/src/github.com/nzt4567/print-messenger/' + path)
