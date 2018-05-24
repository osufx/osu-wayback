import json
import MySQLdb
import MySQLdb.cursors
from flask import Flask, make_response, request, render_template, jsonify
from handlers import update

app = Flask(__name__)

with open("config.json", "r") as f:
	config = json.load(f)

@app.route("/")
@app.route("/home")
def home_index():
	return render_template("index.html")

@app.route("/download")
def download_index():
	return render_template("download.html")

@app.route("/api")
def api_index():
	return render_template("api.html")

@app.route("/api/getUpdate", methods=["GET", "POST"])
def api_update():
	return update.handle(request)

@app.route("/api")
def api_index():
    return render_template("api.html")

if __name__ == "__main__":
	app.run(**config["web"])