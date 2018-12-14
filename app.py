from flask import Flask, jsonify, render_template
from scrape import scrape_mars
from data.model import model

app = Flask(__name__, static_url_path = "/temp", static_folder = "temp")

@app.route("/")
def home():
	return render_template("index.html", data=model.getStoredData()[0])

@app.route('/scrape')
def scrape():
	model.createDataBase(scrape_mars.scrape())
	return 'True'


if __name__ == '__main__':
	app.debug = True
	app.run()