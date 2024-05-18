import json
from pymongo import MongoClient
from bson import json_util

# your MongoDB connection URI
MONGO_URI = ""
DB_NAME = ""
COLLECTION_NAME = ""

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Retrieve JSON documents from MongoDB and exclude _id field
documents = list(collection.find({}, {"_id": 0}))

# Convert merged data into a JSON string using json_util
merged_json = json.dumps(documents, default=json_util.default, indent=4)

# Save the merged JSON data into a new JSON file
with open("sport.json", "w") as json_file:
    json_file.write(merged_json)

print("Merged data saved to 'sport.json'")
