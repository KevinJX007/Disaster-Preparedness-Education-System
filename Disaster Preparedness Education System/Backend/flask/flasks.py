from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import mysql.connector
import sys
sys.stdout.reconfigure(encoding='utf-8')

app = Flask(__name__)
CORS(app)

# Database Configuration
db_config = {
    'user': 'root',
    'password': 'Appukkuttan1*$', 
    'host': 'localhost',
    'database': 'disaster_db'
}

def init_db():
    try:
        conn = mysql.connector.connect(
            user=db_config['user'], 
            password=db_config['password'], 
            host=db_config['host']
        )
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS disaster_db")
        cursor.execute("USE disaster_db")
        
        # TABLE 1: Everyone who registers
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS heroes (
                serial_number INT AUTO_INCREMENT PRIMARY KEY,
                hero_name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL, 
                registration_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # TABLE 2: Only those who finish the course
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS graduates (
                id INT AUTO_INCREMENT PRIMARY KEY,
                hero_name VARCHAR(255) NOT NULL,
                completion_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Database ready!")
    except Exception as e:
        print(f"❌ Error initializing database: {e}")

# --- ROUTES ---

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register_hero', methods=['POST'])
def register_hero():
    data = request.json
    name = data.get('username')
    email = data.get('email')
    
    if not name or not email:
        return jsonify({"error": "Name and Email are required!"}), 400

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        query = "INSERT INTO heroes (hero_name, email) VALUES (%s, %s)"
        cursor.execute(query, (name, email))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": f"Hero {name} registered!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/mark_complete', methods=['POST'])
def mark_complete():
    data = request.json
    name = data.get('username')
    
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Check if already graduated
        check_query = "SELECT * FROM graduates WHERE hero_name = %s"
        cursor.execute(check_query, (name,))
        if cursor.fetchone():
            return jsonify({"message": "Already graduated!"}), 200

        # Insert into graduates table
        query = "INSERT INTO graduates (hero_name) VALUES (%s)"
        cursor.execute(query, (name,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Graduate added!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/graduates')
def show_graduates():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT hero_name, completion_time FROM graduates ORDER BY completion_time DESC")
        graduates = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('graduates.html', students=graduates)
    except Exception as e:
        return f"Error fetching data: {e}"

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)