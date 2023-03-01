from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongodb://mongodb:27017/")

db = client.td6db

collection = db.td6_collection
collection.insert_one({"test":"blaaaaa"})

@app.route('/')
def read_data():
    # retrieve data from MongoDB
    mongo_data = ""
    for data in collection.find():
        mongo_data += str(data) + "<br>"

    # read content from text file
    with open('text_file.txt', 'r') as f:
        text_file_data = f.read()

    # combine the two data sources
    content = mongo_data + text_file_data

    return content

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
