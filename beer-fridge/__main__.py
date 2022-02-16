from flask import Flask, request

from controller import FridgeController

fridgeController = FridgeController()

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World!"

if __name__ == '__main__':
    app.run(debug=True)