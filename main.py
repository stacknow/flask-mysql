from flask import Flask, jsonify, request
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# MySQL database connection
def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="yourUsername",
        password="yourPassword",
        database="yourDatabaseName"
    )
    return connection

# Route to get all users
@app.route('/users', methods=['GET'])
def get_users():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        return jsonify(users)
    except Error as e:
        return jsonify({"error": str(e)})
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Route to create a new user
@app.route('/users', methods=['POST'])
def create_user():
    new_user = request.json
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", 
                       (new_user["name"], new_user["email"]))
        connection.commit()
        return jsonify({"message": "User created", "user_id": cursor.lastrowid})
    except Error as e:
        return jsonify({"error": str(e)})
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Start the Flask server
if __name__ == '__main__':
    app.run(port=5000)
