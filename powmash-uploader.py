from pathlib import PurePath
import subprocess
import tempfile

from flask import Flask, render_template, request, redirect, flash, url_for
from furl import furl
import requests


ALLOWED_EXTENSIONS = ['pptx']
POWMASH_BIN_DIR = '/Users/nyangkun/Projects/PrezMashup/MashupConverter/bin/Release'
POWMASH_BIN_FILENAME = 'MashupConverter.exe'
MONO_FRAMEWORK_PATH = '/Library/Frameworks/Mono.framework/Versions/Current'
NODERED_HOST = 'localhost'
NODERED_PORT = 1880
NODERED_TAB_LABEL = 'PowMash'


app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
furl_nodered = furl().set(scheme='http', host=NODERED_HOST, port=NODERED_PORT)


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
    tab_id_powmash = get_nodered_tab_id()
    if tab_id_powmash is not None:
        delete_nodered_tab(tab_id_powmash)
    create_nodered_tab(flow)


def get_nodered_tab_id():
    f = furl_nodered.copy().add(path='/flows')
    r = requests.get(f.url)
    if r.status_code != 200:
        raise NodeRedError(f.path, r.status_code)
    res = r.json()
    tab_id = None
    for node in res:
        if node['type'] == 'tab' and node['label'] == NODERED_TAB_LABEL:
            tab_id = node['id']
            break
    return tab_id


def delete_nodered_tab(tab_id):
    f = furl_nodered.copy().add(path='/flow/').add(path=tab_id)
    r = requests.delete(f.url)
    if r.status_code != 204:
        raise NodeRedError(f.path, r.status_code)


def create_nodered_tab(flow):
    f = furl_nodered.copy().add(path='/flow')

    def data():
        yield b'{"label":"'
        yield NODERED_TAB_LABEL.encode()
        yield b'","nodes":'
        yield flow
        yield b'}'
    headers = {'Content-Type': 'application/json'}
    r = requests.post(f.url, data=data(), headers=headers)
    if r.status_code not in (200, 204):
        raise NodeRedError(f.path, r.status_code)


class NodeRedError(RuntimeError):
    MSG_FORMAT = "Node-RED HTTP API request to endpoint '{0}' failed with status code {1}"

    def __init__(self, endpoint, status_code):
        msg = self.MSG_FORMAT.format(endpoint, status_code)
        super(NodeRedError, self).__init__(msg)


if __name__ == '__main__':
    app.run()
