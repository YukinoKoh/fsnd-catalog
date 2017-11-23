from flask import Flask, render_template
# app name
app = Flask(__name__)


@app.route('/')
def main():
    return render_template('sample.html')


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    # let hear any webserver
    app.run(host='0.0.0.0', port=5000)
