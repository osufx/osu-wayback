import json
import MySQLdb
import MySQLdb.cursors
from flask import Flask, make_response, request, render_template, jsonify
from handlers import getupdate, getfile
from objects import glob

app = Flask(__name__)

with open("config.json", "r") as f:
	config = json.load(f)

# Setup sql
glob.sql = MySQLdb.connect(**config["sql"], cursorclass = MySQLdb.cursors.DictCursor)

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
	data = getupdate.handle(request)
	return jsonify(data)

@app.route("/api/getFile", methods=["GET", "POST"])
def api_file():
	data = getfile.handle(request)
	return jsonify(data)

if __name__ == "__main__":
	app.run(**config["web"])