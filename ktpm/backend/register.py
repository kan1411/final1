from flask import request, jsonify, Blueprint
import mysql.connector
import logging

bp = Blueprint('register', __name__)


logging.basicConfig(level=logging.DEBUG)

try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Kan-1411",
        database="register"
    )
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            name VARCHAR(255) NOT NULL,
            gender VARCHAR(10) NOT NULL,
            role VARCHAR(10) NOT NULL,
            area VARCHAR(255) NOT NULL,
            phone VARCHAR (20) NOT NULL,
            academic VARCHAR(255) NOT NULL
        )
    """)
    db.commit()
except mysql.connector.Error as err:
    logging.error(f"Error: {err}")

@bp.route('/checkUser', methods=['POST'])
def check_user():
    try:
        data = request.json
        logging.debug(f"Received data for checkUser: {data}")
        
        if not data:
            return jsonify({"error": "No data provided"}), 400

        username = data.get('username')
        phone = data.get('phone')

        cursor = db.cursor()
        query = "SELECT * FROM users WHERE username = %s OR phone = %s"
        cursor.execute(query, (username, phone))
        results = cursor.fetchall()

        if results:
            existing_user = any(user[1] == username for user in results)
            existing_phone = any(user[7] == phone for user in results)

            if existing_user:
                return jsonify({"message": "Username đã tồn tại!"}), 400
            if existing_phone:
                return jsonify({"message": "Số điện thoại đã tồn tại!"}), 400

        return jsonify({"message": "Username và Phone hợp lệ."}), 200
    except mysql.connector.Error as err:
        logging.error(f"Lỗi khi kiểm tra: {err}")
        return jsonify({"message": f"Lỗi khi kiểm tra: {err}"}), 500
    finally:
        cursor.close()

@bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.json 
        logging.debug(f"Received data for register: {data}")
        
        if not data:
            return jsonify({"error": "No data provided"}), 400

        username = data.get('username')
        password = data.get('password')  
        name = data.get('name')
        gender = data.get('gender')
        role = data.get('role')
        area = data.get('area')
        phone = data.get('phone')
        academic = data.get('academic')

        cursor = db.cursor()
        query = "SELECT * FROM users WHERE username = %s OR phone = %s"
        cursor.execute(query, (username, phone))
        results = cursor.fetchall()

        if results:
            existing_user = any(user[1] == username for user in results)
            existing_phone = any(user[7] == phone for user in results)

            if existing_user:
                return jsonify({"message": "Username đã tồn tại!"}), 400
            if existing_phone:
                return jsonify({"message": "Phone đã tồn tại!"}), 400

        query = """
            INSERT INTO users (username, password, name, gender, role, area, phone, academic)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (username, password, name, gender, role, area, phone, academic)
        cursor.execute(query, values)
        db.commit()
        response = {'message': 'Đăng ký thành công rồi, bạn giỏi quá!!!'}
    except mysql.connector.Error as err:
        logging.error(f"Lỗi khi đăng ký: {err}")
        response = {'message': f'Lỗi khi đăng ký: {err}'}
    finally:
        cursor.close()
    return jsonify(response)

if db.is_connected():
    print("Kết nối thành công đến cơ sở dữ liệu MySQL.")
else:
    print("Kết nối không thành công đến cơ sở dữ liệu MySQL.")

