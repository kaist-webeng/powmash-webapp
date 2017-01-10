from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/deploy', methods=['GET',])
def deploy():
    return render_template('deploy.html')


if __name__ == '__main__':
    app.run()
