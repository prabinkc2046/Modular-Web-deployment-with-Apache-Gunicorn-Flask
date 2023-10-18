from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, this is the Flask app running on a dedicated server!"
