from flask import Flask

app = Flask(__name__)

@app.route("/hello")
def hello():
    return "Hello World!"

@app.route("/usr/<name>")
def hello1(name):
    return "Hello World! {}" .format(name)


if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 80)