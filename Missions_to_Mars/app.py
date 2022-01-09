from flask import Flask, render_template, redirect
from flask_pymongo import pymongo
import scrape_mars

app = Flask(__name__)

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

mongo = pymongo(app, uri="mongodb://localhost:27017/mars_db")

@app.route("/")
def index():
    mars_dict = mongo.db.mars_dict.find_one()
    return render_template("index.html", mars_dict=mars_dict)

@app.route("/scrape")
def scrape():
    mars_dict = mongo.db.mars_dict
    mars_data = scrape_mars.scrape()
    mars_dict.update({}, mars_data, upsert=True)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)