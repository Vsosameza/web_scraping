from missiontomars import scrape
import pymongo
from flask import Flask, jsonify, render_template

# client = pymongo.MongoClient()
# db = client.marsdb
# collection = db.marsdb.marscollection

app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb://localhost:27017/marsdb"
mongo = Pymongo(App)

@app.route("/")
def index():
    mars_data = mongo.db.marsdb.find_one(
    sort = [('_id', -1)]    
    )
    return render_template('index.html', mars_data = mars_data)


@app.route("/scrape")
def insert_and_redirect():
    for_insert = scrape()
    mongo.db.marsdb.insert_one(for_insert)
    
    #print(data)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)