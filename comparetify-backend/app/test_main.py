from flask import Flask  # type: ignore

app = Flask(__name__)

@app.route('/test')
def hello_world():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)
