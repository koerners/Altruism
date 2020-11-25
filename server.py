import json

from flask import Flask, jsonify, render_template
from flask_cors import cross_origin

from main import run_sim

app = Flask(__name__, static_folder="visualisation", template_folder="visualisation")


@app.route("/agents")
@cross_origin()
def output():
    with open('./out/agents.json') as json_file:
        data = json.load(json_file)
    return jsonify(data)


@app.route("/current")
@cross_origin()
def res_out():
    with open('./out/current.json') as json_file:
        data = json.load(json_file)
    return jsonify(data)


@app.route("/")
@cross_origin()
def out():
    return render_template('index.html')


@app.route("/start")
@cross_origin()
def start():
    run_sim(lag=True)
    return jsonify(start="true")


if __name__ == "__main__":
    app.run()
