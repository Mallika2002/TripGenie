import json
from flask import Flask, jsonify, redirect, render_template, request, url_for, session
import subprocess
import os
from flask_pymongo import PyMongo
from bson import ObjectId
import secrets


app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/tripdb'
mongo = PyMongo(app)

# Route to store user's geolocation in MongoDB
@app.route('/store_location', methods=['POST'])
def store_location():
    data = request.json
    username = data.get('username')
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    # Update or insert location data in MongoDB
    mongo.db.users.update_one(
        {'username': username},
        {'$set': {'location': {'latitude': latitude, 'longitude': longitude}}},
        upsert=True
    )

    return jsonify({'status': 'success'})


# Route to retrieve user's geolocation from MongoDB
@app.route('/get_location/<user_id>', methods=['GET'])
def get_location(user_id):
    location_data = mongo.db.user_locations.find_one({'user_id': user_id}, {'_id': 0})
    return jsonify(location_data)

# Flag to check if Streamlit app is already running
streamlit_running = False


@app.route('/logout')
def logout():
    
    session.pop('username', None)
    
    return redirect(url_for('index'))

# Load the username from the user_data.txt file
def load_username_from_file():

    with open('user_data.txt', 'r') as file:
        username = file.read().strip()
    return username
    
@app.route('/user/<username>/account_details')
def account_details_with_username(username):
    return render_template('cc_index.html')

@app.route('/account_details')
def account_details():
        if 'username' in session:
            username = session['username']
            # Redirect to the route with username included
            return redirect(url_for('account_details_with_username', username=username))
        else:
            return render_template('cc_index.html')
        


@app.route('/add_review')
def add_review():
    return render_template('add_review.html')

@app.route('/trip_details',methods=['POST','GET'])
def trip_details():
    return render_template('trips_index.html')

# Define a route to handle form submission
@app.route('/update-profile', methods=['POST'])
def update_profile():
    user_data = {
        "name": request.form.get('name'),
        "email": request.form.get('email'),
        "currentPassword": request.form.get('currentPassword'),
        "newPassword": request.form.get('newPassword'),
        "repeatPassword": request.form.get('repeatPassword'),
        "bio": request.form.get('bio'),
        "birthday": request.form.get('birthday'),
        "gender": request.form.get('gender'),
        "phone": request.form.get('phone')
    }
    username_from_file = load_username_from_file()
    print(username_from_file)


    # Fetch user from MongoDB using the username from the session
    user = mongo.db.users.find_one({"username": username_from_file})

    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # Check current password if provided
    if user_data["currentPassword"] and user_data["currentPassword"] != user["password"]:
        error_message = "Incorrect current password"
        return render_template('cc_index.html', error_message=error_message)

    # Update user fields
    update_fields = {}
    if user_data["name"] is not None and user_data["name"] != "":
        update_fields["name"] = user_data["name"]
    if user_data["email"] is not None and user_data["email"] != "":
        update_fields["email"] = user_data["email"]
    if user_data["bio"] is not None and user_data["bio"] != "":
        update_fields["bio"] = user_data["bio"]
    if user_data["birthday"] is not None and user_data["birthday"] != "":
        update_fields["birthday"] = user_data["birthday"]
    if user_data["gender"] is not None and user_data["gender"] != "":
        update_fields["gender"] = user_data["gender"]
    if user_data["phone"] is not None and user_data["phone"] != "":
        update_fields["phone"] = user_data["phone"]


    print("Content of update_fields:", user_data)
    print(user_data["newPassword"])
    print(user_data["repeatPassword"])
    # Update password only if a new password is provided
    if user_data["newPassword"] and user_data["newPassword"] == user_data["repeatPassword"]:
        mongo.db.users.update_one(
        {"username": username_from_file},
        {"$set": {"password": user_data["newPassword"]}}
    )

    # Save the updated user document
    mongo.db.users.update_one(
    {"username": username_from_file},
    {
        "$set": update_fields,
        "$setOnInsert": {"username": username_from_file}
    },
    upsert=True
    )
    
    return render_template('cc_index.html', alert="Profile updated successfully", success=True)


@app.route('/store_address', methods=['POST'])
def store_address():
    data = request.json
    username = data.get('username')
    address = data.get('address')
        
    mongo.db.users.update_one(
        {'username': username},
        {'$set': {'location.address': address}},
        upsert=True
    )

    return jsonify({'status': 'success'})

@app.route('/user/<username>')
def user_page(username):
    return render_template('index.html', username=username)

@app.route('/')
def index():
    if 'username' in session:
        print('HI')
        return redirect(url_for('user_page', username=session['username']))
        # return render_template('index.html', username=session['username'])
    else:
        print('hO')
        shared_data_path = os.path.join(os.path.dirname(__file__), 'user_data.txt')
        with open(shared_data_path, 'w',encoding='utf-8') as file:
            pass

        return render_template('index.html')



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.json.get('username')
        password = request.json.get('password')
        dob = request.json.get('dob')

        # Validate the form data if needed

        # Store user data in MongoDB
        mongo.db.users.insert_one({'username': username, 'password': password, 'dob': dob})

        return jsonify({'status':'success'})

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.json.get('username')
        password = request.json.get('password')

        user_data = mongo.db.users.find_one({'username': username, 'password': password})

        if user_data:
            session['username'] = username  # Store username in session

            shared_data_path = os.path.join(os.path.dirname(__file__), 'user_data.txt')
            with open(shared_data_path, 'w',encoding='utf-8') as file:
                file.write(f"{session.get('username')}")
                
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'error'})
    else:
        return render_template('login.html')
    



@app.route('/save_changes', methods=['POST'])
def save_changes():
    if 'username' in session:
        username = session['username']

        # Retrieve form data from the request
        username_input = request.form.get('username')
        name = request.form.get('name')
        email = request.form.get('email')

        print(username)
        print(name)
        print(email)
        
        # Add more fields as needed based on your form

        # Update the user data in MongoDB
        mongo.db.users.update_one(
            {'username': username},
            {'$set': {'username': username_input, 'name': name, 'email': email}},
        )

        # Redirect back to the account details page

        
        return redirect(url_for('account_details'))
    else:
        # Handle the case where the username is not in the session
        return redirect(url_for('index'))
    

@app.route('/book')
def book():
        
        if 'username' in session:
        # Store the current URL in the session
            session['previous_url'] = url_for('user_page', username=session['username'])

            code_path = os.path.abspath("streamlit/code.py")
            subprocess.Popen(["streamlit", "run", code_path])

            # Redirect back to the user's page
            return redirect(session.pop('previous_url', url_for('index')))
        else:

            code_path = os.path.abspath("streamlit/code.py")
            subprocess.Popen(["streamlit", "run", code_path])
            # Handle the case where the username is not in the session
            return redirect(url_for('index'))
        

@app.route('/streamlit')
def streamlit():
    global streamlit_running

    if not streamlit_running and request.args.get('action') == 'plan_a_tour':
        code_path = os.path.abspath("streamlit/code.py")
        subprocess.Popen(["streamlit", "run", code_path])
        streamlit_running = True

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
