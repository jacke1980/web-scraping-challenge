from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import sys

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/Mission_to_Mars_db"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/phone_app")


@app.route("/")
def index():
    print('I am on index.html')
    mars_data = mongo.db.mars_db.find_one()
    return render_template("index.html", data=mars_data)


@app.route("/scrape")
def scraper():
    print("I am in scrape")
    mars_info=scrape_mars.mars_news_scrape()
    mars_info=scrape_mars.img_scrape()
    mars_info=scrape_mars.mars_facts()
    mars_info=scrape_mars.marshemispheres()
    mongo.db.mars_db.collection.update({},{"$set": mars_info},upsert=True)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
