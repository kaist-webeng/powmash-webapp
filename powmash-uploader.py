from pathlib import PurePath
import subprocess
import tempfile

from flask import Flask, render_template, request, redirect, flash, url_for


ALLOWED_EXTENSIONS = ['pptx']
POWMASH_BIN_DIR = '/Users/nyangkun/Projects/PrezMashup/MashupConverter/bin/Release'
POWMASH_BIN_FILENAME = 'MashupConverter.exe'
MONO_FRAMEWORK_PATH = '/Library/Frameworks/Mono.framework/Versions/Current'


app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/deploy', methods=['GET',])
def deploy():
    return render_template('deploy.html')


@app.route('/deploy', methods=['POST',])
def deploy_post():
    if 'mashup_file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['mashup_file']
    # if user does not select file, browser also
    # submit a empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        with tempfile.NamedTemporaryFile() as tf:
            file.save(tf.name)
            try:
                flow = execute_converter(tf)
                deploy_to_nodered(flow)
            except ValueError as e:
                flash(e)
                return redirect(request.url)
        return redirect(url_for('control'))
    flash('File extension not allowed')
    return redirect(request.url)


@app.route('/control', methods=['GET'])
def control():
    return "TBD"


def execute_converter(file):
    mono_path = PurePath(MONO_FRAMEWORK_PATH, 'bin', 'mono')
    powmash_bin_path = PurePath(POWMASH_BIN_DIR, POWMASH_BIN_FILENAME)
    cp = subprocess.run([str(mono_path), str(powmash_bin_path), '-i', file.name],
                        cwd=POWMASH_BIN_DIR,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)
    if cp.returncode != 0:
        raise ValueError(cp.stderr)
    return cp.stdout


def deploy_to_nodered(flow):
    pass


if __name__ == '__main__':
    app.run()
