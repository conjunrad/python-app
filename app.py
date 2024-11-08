from flask import Flask, jsonify, request
import mysql.connector
import os

app = Flask(__name__)

DB_CONFIG = {
  'host': os.getenv('MYSQL_HOST', 'mysql'),
  'user': os.getenv('MYSQL_USER', 'root'),
  'password': os.getenv('MYSQL_PASSWORD', 'password'),
  'database': os.getenv('MYSQL_DATABASE', 'flaskdb')
}

@app.route('/', methods=['GET'])
def index():
  return jsonify({'message': 'Hello world!'}), 200

@app.route('/users', methods=['GET'])
def get_users():
  try:
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return jsonify(users, 200)
  except Exception as e:
    return jsonify({'error': str(e)}), 500
  finally:
    if conn.is_connected():
      cursor.close()
      conn.close()

@app.route('/users', methods=['POST'])
def add_user():
  try:
    data = request.get_json()

    name = data['name']
    email = data['email']

    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    cursor.execute('INSERT INTO users (name, email) VALUES (%s, %s)', (name, email))
    cursor.commit()
    return jsonify({'meesage': f'User {name} created successfully'}), 201
  except Exception as e:
    return jsonify({'error': str(e)}), 500
  finally:
    if conn.is_connected():
      cursor.close()
      conn.close()

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8000)
