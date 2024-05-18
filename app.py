from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection string
mongo_uri = ""
client = MongoClient(mongo_uri)
db = client[""]
messages = db[""]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    message = data['message']
    
    # Insert the message into MongoDB
    messages.insert_one({'message': message})
    return jsonify({'message': message})

@app.route('/update_message', methods=['POST'])
def update_message():
    data = request.get_json()
    message = data['message']

    # Update the message in MongoDB
    messages.update_one({}, {'$set': {'message': message}})
    return jsonify({'message': message})

if __name__ == '__main__':
    app.run(debug=True)
