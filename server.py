from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb://mongo:27017/')  # Connect to MongoDB service named 'mongo' within Docker network
db = client['bytehr_database']  # Connect to 'bytehr_database' database
collection = db['data_collection']  # Access 'data_collection' collection within the database

# Endpoint to render the form
@app.route('/')
def index():
    return render_template('index.html')

# Endpoint to create data
@app.route('/data', methods=['POST'])
def create_data():
    data = {
        'name': request.form['name'],
        'age': int(request.form['age'])
    }
    result = collection.insert_one(data)  # Insert data into MongoDB collection
    return jsonify({"message": "Data created successfully", "_id": str(result.inserted_id)})  # Return response

# Endpoint to get all data
@app.route('/data', methods=['GET'])
def get_all_data():
    data = list(collection.find())  # Retrieve all data from MongoDB collection
    return jsonify(data)  # Return data as JSON response

# Endpoint to get data by ID
@app.route('/data/<data_id>', methods=['GET'])
def get_data(data_id):
    data = collection.find_one({"_id": ObjectId(data_id)})  # Find data by ID in MongoDB collection
    if data:
        return jsonify(data)  # Return data as JSON response
    else:
        return jsonify({"error": "Data not found"}), 404  # Return error if data not found

# Endpoint to update data by ID
@app.route('/data/<data_id>', methods=['PUT'])
def update_data(data_id):
    data = {
        'name': request.form['name'],
        'age': int(request.form['age'])
    }
    result = collection.update_one({"_id": ObjectId(data_id)}, {"$set": data})  # Update data in MongoDB collection
    if result.modified_count:
        return jsonify({"message": "Data updated successfully"})
    else:
        return jsonify({"error": "Data not found"}), 404  # Return error if data not found

# Endpoint to delete data by ID
@app.route('/data/<data_id>', methods=['DELETE'])
def delete_data(data_id):
    result = collection.delete_one({"_id": ObjectId(data_id)})  # Delete data by ID from MongoDB collection
    if result.deleted_count:
        return jsonify({"message": "Data deleted successfully"})
    else:
        return jsonify({"error": "Data not found"}), 404  # Return error if data not found

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')  # Run Flask app in debug mode, listen on all interfaces
