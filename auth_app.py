from flask import Flask, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_session import Session
import re

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

users_db = {}

password_pattern = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$')

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Debugging: Print received data
    print(f"Received registration data: Username = {username}, Password = {password}")

    if not username or not password:
        print("Error: Missing username or password.")
        return jsonify({'error': 'Username and password are required.', 'statusCode': 400}), 400

    if username in users_db:
        print("Error: User already exists.")
        return jsonify({'error': 'User already exists.', 'statusCode': 400}), 400

    if not password_pattern.match(password):
        print("Error: Password does not match the required pattern.")
        return jsonify({'error': 'Password must be at least 8 characters long, contain one letter and one number.', 'statusCode': 400}), 400

    # Debugging: Show password before hashing
    print(f"Password before hashing: {password}")

    # Hash the password and store the user
    hashed_password = generate_password_hash(password)
    users_db[username] = hashed_password

    print("User registered successfully.")
    return jsonify({'message': 'User registered successfully!', 'statusCode': 201}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required.', 'statusCode': 400}), 400

    # Check if user exists
    hashed_password = users_db.get(username)
    if not hashed_password or not check_password_hash(hashed_password, password):
        return jsonify({'error': 'Invalid username or password.', 'statusCode': 401}), 401

    # Set session
    session['username'] = username
    return jsonify({'message': 'Logged in successfully!', 'statusCode': 200}), 200

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return jsonify({'message': 'Logged out successfully!', 'statusCode': 200}), 200

@app.route('/protected', methods=['GET'])
def protected():
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized access, please login.', 'statusCode': 401}), 401
    return jsonify({'message': f'Hello, {session["username"]}! Welcome to the protected route.', 'statusCode': 200}), 200

if __name__ == '__main__':
    app.run(debug=True)