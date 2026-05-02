from flask import Flask, jsonify, request
import pymysql

app = Flask(name)

# =========================
# RDS MASTER / WRITER CONFIG
# =========================
RDS_HOST = 'ali.cj4scy2wmhq4.us-east-1.rds.amazonaws.com'  # updated endpoint
RDS_USER = 'admin'
RDS_PASSWORD = 'Root1234'  # updated password
RDS_DB_NAME = 'dev'
TABLE_NAME = 'users'

# =========================
# GET ALL USERS
# =========================
@app.route('/users', methods=['GET'])
def get_users():
    try:
        connection = pymysql.connect(
            host=RDS_HOST,
            user=RDS_USER,
            password=RDS_PASSWORD,
            database=RDS_DB_NAME,
            cursorclass=pymysql.cursors.DictCursor
        )
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {TABLE_NAME} LIMIT 10;")
            users = cursor.fetchall()
        return jsonify(users)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if 'connection' in locals():
            connection.close()

# =========================
# ADD NEW USER (POST)
# =========================
@app.route('/users', methods=['POST'])
def add_user():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')

        if not name or not email:
            return jsonify({"error": "Missing 'name' or 'email'"}), 400

        connection = pymysql.connect(
            host=RDS_HOST,
            user=RDS_USER,
            password=RDS_PASSWORD,
            database=RDS_DB_NAME,
            cursorclass=pymysql.cursors.DictCursor
        )
        with connection.cursor() as cursor:
            sql = f"INSERT INTO {TABLE_NAME} (name, email) VALUES (%s, %s)"
            cursor.execute(sql, (name, email))
            connection.commit()

        return jsonify({"message": "User added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if 'connection' in locals():
            connection.close()

# =========================
# UPDATE USER (PUT)
# =========================
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')

        if not name and not email:
            return jsonify({"error": "Provide at least 'name' or 'email'"}), 400

        connection = pymysql.connect(
            host=RDS_HOST,
            user=RDS_USER,
            password=RDS_PASSWORD,
            database=RDS_DB_NAME,
            cursorclass=pymysql.cursors.DictCursor
        )
        with connection.cursor() as cursor:
            sql = f"UPDATE {TABLE_NAME} SET name=%s, email=%s WHERE id=%s"
            cursor.execute(sql, (name, email, user_id))
            connection.commit()

            if cursor.rowcount == 0:
                return jsonify({"error": "User not found"}), 404

        return jsonify({"message": "User updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if 'connection' in locals():
            connection.close()

# =========================
# DELETE USER (DELETE)
# =========================
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        connection = pymysql.connect(
            host=RDS_HOST,
            user=RDS_USER,
            password=RDS_PASSWORD,
            database=RDS_DB_NAME,
            cursorclass=pymysql.cursors.DictCursor
        )
        with connection.cursor() as cursor:
            sql = f"DELETE FROM {TABLE_NAME} WHERE id=%s"
            cursor.execute(sql, (user_id,))
            connection.commit()

            if cursor.rowcount == 0:
                return jsonify({"error": "User not found"}), 404

        return jsonify({"message": "User deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if 'connection' in locals():
            connection.close()
			
# =========================
# Health Check
# =========================
@app.route('/')
def index():
    return "RDS Master API running"

# =========================
# Entry Point
# =========================
if name == 'main':
    app.run(host='0.0.0.0', port=5000, debug=True)