from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# Database Configuration
db_config = {
    'user': 'root',
    'password': 'Appukkuttan1*$', # 👈 Change this to your MySQL password
    'host': 'localhost',
    'database': 'disaster_preparedness'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

# Initialize Database and Tables
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS disaster_preparedness")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS heroes (
            id INT serial PRIMARY KEY,
            username VARCHAR(255))
    """)
    conn.commit()
    cursor.close()
    conn.close()

@app.route('/save_hero', methods=['POST'])
def save_hero():
    data = request.json
    username = data.get('username')
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
        
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({"message": "Hero Progress Saved to MySQL!"})

if __name__ == '__main__':
    init_db() # Run table creation on start
    app.run(debug=True)
