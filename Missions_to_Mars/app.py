from flask import Flask, render_template, redirect, jsonify
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)


app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)


@app.route("/")
def index():
    mars_dict = mongo.db.collection.find_one()
    return render_template("index.html", mars_dict=mars_dict)

@app.route("/scrape")
def scrape():
    #mars_dict = mongo.db.mars_dict
    mars_data = scrape_mars.scrape()
    mongo.db.collection.update({}, {"$set": mars_data}, upsert=True)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)