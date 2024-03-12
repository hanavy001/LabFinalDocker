from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb://mongo:27017/')
db = client['bytehr_database']
collection = db['data_collection']

# Route to display the form for creating data
@app.route('/create', methods=['GET'])
def create_page():
    return render_template('create_data.html')

# Route to handle creation of data
@app.route('/create', methods=['POST'])
def create_data():
    try:
        data = {
            'name': request.form['name'],
            'age': int(request.form['age'])
        }
        result = collection.insert_one(data)
        return "Data created successfully", 201
    except Exception as e:
        return str(e), 400

# Route to display the form for getting data by ID
@app.route('/get', methods=['GET'])
def get_page():
    return render_template('get_data.html')

# Route to handle getting data by ID
@app.route('/get', methods=['POST'])
def get_data():
    data_id = request.form['data_id']
    data = collection.find_one({"_id": ObjectId(data_id)})
    if data:
        # Convert ObjectId to string before returning JSON
        data['_id'] = str(data['_id'])
        return jsonify(data)
    else:
        return jsonify({"error": "Data not found"}), 404

# Route to display the form for updating data by ID
@app.route('/update', methods=['GET'])
def update_page():
    return render_template('update_data.html')

# Route to handle updating data by ID
@app.route('/update', methods=['POST'])
def update_data():
    try:
        data_id = request.form['data_id']
        data = {
            'name': request.form['name'],
            'age': int(request.form['age'])
        }
        result = collection.update_one({"_id": ObjectId(data_id)}, {"$set": data})
        if result.modified_count:
            return "Data updated successfully", 204
        else:
            return "Data not found", 404
    except Exception as e:
        return str(e), 400

# Route to display the form for deleting data by ID
@app.route('/delete', methods=['GET'])
def delete_page():
    return render_template('delete_data.html')

# Route to handle deleting data by ID
@app.route('/delete', methods=['POST'])
def delete_data():
    try:
        data_id = request.form['data_id']
        result = collection.delete_one({"_id": ObjectId(data_id)})
        if result.deleted_count:
            return "Data deleted successfully", 204
        else:
            return "Data not found", 404
    except Exception as e:
        return str(e), 400

# Route to display the form for getting all data
@app.route('/get_all', methods=['GET'])
def get_all_page():
    try:
        all_data = list(collection.find())
        return render_template('get_all_data.html', all_data=all_data)
    except Exception as e:
        return str(e), 400

# Route for the index page
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
