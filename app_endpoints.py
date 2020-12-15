from flask import Flask
# creating the application end points . this is app will showcase "Hello World" on an html page

app = Flask(__name__)

@app.route('/')
def show():
    
    return 'Hello World!'

app.run(port = 5000)
