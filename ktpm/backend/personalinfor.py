from flask import Flask, jsonify, request, render_template, Blueprint
import mysql.connector
import logging

app = Flask(__name__)

bp = Blueprint('personalinfor', __name__)

logging.basicConfig(level=logging.DEBUG)

db_status = "Chưa kết nối đến MySQL."

try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Kan-1411",
        database="register"
    )
    if db.is_connected():
        db_status = "Kết nối thành công đến cơ sở dữ liệu MySQL."
        logging.info(db_status)
except mysql.connector.Error as err:
    db_status = f"Lỗi kết nối đến cơ sở dữ liệu MySQL: {err}"
    logging.error(db_status)

@bp.route('/')
def home():
    return render_template('personalinfor.html', db_status=db_status)

@bp.route('/userinfo', methods=['GET'])
def get_user_info():
    username = request.args.get('username')
    
    if not username:
        return jsonify(), 400
    
    cursor = db.cursor(dictionary=True)
    query = "SELECT username, name, gender, role, area, phone, academic FROM users WHERE username = %s"
    logging.debug(f"Executing query: {query} with username={username}")
    
    try:
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        logging.debug(f"Query result: {result}")
    except mysql.connector.Error as err:
        logging.error(f"SQL Error: {err}")
        return jsonify({"error": "Database query error"}), 500
    finally:
        cursor.close()

    if result:
        return jsonify(result)
    else:
        return jsonify({"error": "User not found"}), 404

@bp.route('/update_userinfo', methods=['POST'])
def update_user_info():
    data = request.get_json()
    logging.debug(f"Received update data: {data}")
    username = data.get('username')
    password = data.get('password')
    confirm_password = data.get('confirm_password')
    name = data.get('name')
    gender = data.get('gender')
    role = data.get('role')
    area = data.get('area')
    phone = data.get('phone')
    academic = data.get('academic')

    if password != confirm_password:
        return jsonify({"error": "Mật khẩu không khớp!"}), 400

    cursor = db.cursor(dictionary=True)

    query = "SELECT * FROM users WHERE phone = %s AND username != %s"
    cursor.execute(query, (phone, username))
    if cursor.fetchone():
        cursor.close()
        return jsonify({"error": "Số điện thoại đã tồn tại!"}), 400

    query = """
        UPDATE users
        SET password = %s, name = %s, gender = %s, role = %s, area = %s, phone = %s, academic = %s
        WHERE username = %s
    """
    try:
        cursor.execute(query, (password, name, gender, role, area, phone, academic, username))
        db.commit()
        return jsonify({"success": "User info updated successfully"})
    except mysql.connector.Error as err:
        logging.error(f"SQL Error: {err}")
        return jsonify({"error": "Database update error"}), 500
    finally:
        cursor.close()

app.register_blueprint(bp, url_prefix='/')


