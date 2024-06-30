from flask import jsonify, request, send_from_directory, Blueprint
import mysql.connector
import logging

bp = Blueprint('classinfor', __name__)

logging.basicConfig(level=logging.DEBUG)

def get_db_connection():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Kan-1411",
            database="register"
        )
        if db.is_connected():
            logging.info("Kết nối thành công đến cơ sở dữ liệu MySQL.")
            return db
    except mysql.connector.Error as err:
        logging.error(f"Lỗi kết nối đến cơ sở dữ liệu MySQL: {err}")
        return None

@bp.route('/my_classes', methods=['GET'])
def get_my_classes():
    username = request.args.get('username', type=str)

    query = "SELECT * FROM form WHERE username = %s"
    db = get_db_connection()
    if db:
        cursor = db.cursor(dictionary=True)
        cursor.execute(query, (username,))
        classes = cursor.fetchall()
        cursor.close()
        db.close()
        return jsonify(classes)
    else:
        return jsonify({"error": "Không thể kết nối đến cơ sở dữ liệu"}), 500

@bp.route('/registered_classes', methods=['GET'])
def get_registered_classes():
    username = request.args.get('username', type=str)

    query = """
        SELECT f.*, u.name AS registered_by_name 
        FROM form f 
        LEFT JOIN users u ON f.registered_by = u.username 
        WHERE f.registered_by = %s
    """
    db = get_db_connection()
    if db:
        cursor = db.cursor(dictionary=True)
        cursor.execute(query, (username,))
        classes = cursor.fetchall()
        cursor.close()
        db.close()
        return jsonify(classes)
    else:
        return jsonify({"error": "Không thể kết nối đến cơ sở dữ liệu"}), 500

@bp.route('/register_class', methods=['POST'])
def register_class():
    data = request.json
    class_id = data.get('class_id')
    username = data.get('username')

    query = "UPDATE form SET registered_by = %s WHERE id = %s"
    db = get_db_connection()
    if db:
        cursor = db.cursor()
        cursor.execute(query, (username, class_id))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({"message": "Đăng ký thành công"})
    else:
        return jsonify({"error": "Không thể kết nối đến cơ sở dữ liệu"}), 500

@bp.route('/get_user_info', methods=['GET'])
def get_user_info():
    username = request.args.get('username', type=str)

    query = "SELECT * FROM users WHERE username = %s"
    db = get_db_connection()
    if db:
        cursor = db.cursor(dictionary=True)
        cursor.execute(query, (username,))
        user_info = cursor.fetchone()
        cursor.close()
        db.close()
        return jsonify(user_info)
    else:
        return jsonify({"error": "Không thể kết nối đến cơ sở dữ liệu"}), 500

@bp.route('/accept_registration', methods=['POST'])
def accept_registration():
    data = request.json
    class_id = data.get('class_id')
    db = get_db_connection()
    if db:
        cursor = db.cursor()
        query = "UPDATE form SET status = 'Đã được nhận' WHERE id = %s"
        cursor.execute(query, (class_id,))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({"message": "Nhận lớp thành công"})
    else:
        return jsonify({"error": "Không thể kết nối đến cơ sở dữ liệu"}), 500

@bp.route('/<path:path>')
def serve_page(path):
    return send_from_directory('.', path)
