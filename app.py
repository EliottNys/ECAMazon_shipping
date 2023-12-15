from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask import render_template
import os
import requests

app = Flask(__name__)
app.config['MONGO_URI'] = os.environ.get('MONGO_URI', 'mongodb://shipping-mongodb:27017/shipping_db')
mongo = PyMongo(app)

# Parcel search by parcel ID
@app.route('/')
def search():
    return render_template('search.html')

# Add a new parcel (for STOCK microservice)
@app.route('/new_parcel', methods=['POST'])
def new_parcel():
    data = request.json
    try:
        order_id = data['order_id']
        user_id = data['user_id']
        parcel_id = data['parcel_id']
    except KeyError:
        return jsonify({'error': 'Missing data'}), 400

    # get address
    user_address = get_user_address(user_id)
    if not user_address:
        return jsonify({'error': 'User address not found'}), 404

    # save to db
    status = 'Processing'
    mongo.db.parcels.insert_one({'parcel_id': parcel_id, 'order_id': order_id, 'user_id': user_id, 'address': user_address, 'status': status})

    # send new parcel to dispatching
    send_to_dispatching(parcel_id, user_address)

    return jsonify({'message': 'Parcel information received successfully'})

# Display all parcels
@app.route('/all_parcels')
def all_parcels():
    try:
        page_size = 10
        page = int(request.args.get('page', 1))
        skip = (page - 1) * page_size

        parcel_data = mongo.db.parcels.find().skip(skip).limit(page_size)

        total_parcels = mongo.db.parcels.count_documents({})
        total_pages = (total_parcels + page_size - 1) // page_size

    except Exception as e:
        return str(e), 500
    return render_template('all_parcels.html', parcel_data=parcel_data, page=page, total_pages=total_pages)

@app.route('/user/<int:user_id>')
def user_parcels(user_id):
    try:
        page_size = 10
        page = int(request.args.get('page', 1))
        skip = (page - 1) * page_size

        user_parcel_data = mongo.db.parcels.find({'user_id': user_id}).skip(skip).limit(page_size)

        total_user_parcels = mongo.db.parcels.count_documents({'user_id': user_id})
        total_user_pages = (total_user_parcels + page_size - 1) // page_size

    except Exception as e:
        return str(e), 500
    
    if total_user_parcels > 0:
        return render_template('user_parcels.html', parcel_data=user_parcel_data, page=page, total_pages=total_user_pages, user_id=user_id)
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/order/<int:order_id>')
def order_parcels(order_id):
    try:
        page_size = 10
        page = int(request.args.get('page', 1))
        skip = (page - 1) * page_size

        order_parcel_data = mongo.db.parcels.find({'order_id': order_id}).skip(skip).limit(page_size)

        total_order_parcels = mongo.db.parcels.count_documents({'order_id': order_id})
        total_order_pages = (total_order_parcels + page_size - 1) // page_size

    except Exception as e:
        return str(e), 500

    if total_order_parcels > 0:
        return render_template('order_parcels.html', parcel_data=order_parcel_data, page=page, total_pages=total_order_pages, order_id=order_id)
    else:
        return jsonify({'error': 'Order not found'}), 404

# Display parcel associated with parcel ID
@app.route('/parcel/<int:parcel_id>', methods=['GET'])
def get_parcel_info(parcel_id):
    parcel_info = mongo.db.parcels.find_one({'parcel_id': parcel_id})

    if parcel_info:
        return render_template('parcel.html', parcel_info=parcel_info)
    else:
        return jsonify({'error': 'Parcel not found'}), 404

# Update the status of a parcel (for DISPATCHING microservice)    
@app.route('/update_status', methods=['POST'])
def update_status():
    data = request.json
    try:
        parcel_id = data['parcel_id']
        new_status = data['status']
    except KeyError:
        return jsonify({'error': 'Missing data'}), 400

    # update status in the database
    result = mongo.db.parcels.update_one({'parcel_id': parcel_id}, {'$set': {'status': new_status}})

    if result.modified_count > 0:
        return jsonify({'message': 'Parcel status updated successfully'})
    else:
        return jsonify({'error': 'Parcel not found'}), 404
    
# Send relevant parcel information to DISPATCHING microservice
def send_to_dispatching(parcel_id, address):
    # =============================
    # call DISPATCHING microservice
    # POST parcel_id and address
    # =============================
    # requests.post("/colis", json= {"parcel_id": parcel_id, "user_address": address})
    pass

# Get user address based on user ID from USERS microservice
def get_user_address(user_id):
    # =============================
    # call USERS microservice
    # GET address from user_id
    # =============================
    # response = requests.get("/users/" + user_id)
    return 'Unknown'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

