from flask import request, jsonify, Blueprint
import mysql.connector
import logging

bp = Blueprint('ad', __name__)

logging.basicConfig(level=logging.DEBUG)

try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Kan-1411",
        database="register"
    )
    if db.is_connected():
        logging.info("Kết nối thành công đến cơ sở dữ liệu MySQL.")
except mysql.connector.Error as err:
    logging.error(f"Error: {err}")

@bp.route('/adlogin', methods=['POST'])
def login():
    try:
        data = request.json
        logging.debug(f"Received data for login: {data}")

        if not data:
            return jsonify({"error": "No data provided"}), 400

        username = data.get('username')
        password = data.get('password')
        
        logging.debug(f"Username: {username}, Password: {password}")

        cursor = db.cursor(dictionary=True)
        query = "SELECT * FROM admin WHERE username = %s AND password = %s"
        logging.debug(f"Executing query: {query} with username: {username} and password: {password}")
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        
        logging.debug(f"Query result: {user}")

        if user:
            response = {'message': 'Đăng nhập thành công!', 'name': user['username'], 'username': user['username']}
        else:
            response = {'message': 'Tài khoản hoặc mật khẩu lỗi'}, 401
    except mysql.connector.Error as err:
        logging.error(f"Lỗi khi đăng nhập: {err}")
        response = {'message': f'Lỗi khi đăng nhập: {err}'}, 500
    finally:
        cursor.close()
    return jsonify(response)

