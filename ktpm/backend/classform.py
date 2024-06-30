from flask import request, jsonify, Blueprint
import mysql.connector
import logging

bp = Blueprint('classform', __name__)

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
        CREATE TABLE IF NOT EXISTS form (
            id INT AUTO_INCREMENT PRIMARY KEY,
            object VARCHAR(255) NOT NULL,
            subject VARCHAR(255) NOT NULL,
            grade VARCHAR(255) NOT NULL,
            gender VARCHAR(255) NOT NULL,
            area VARCHAR(255) NOT NULL,
            cond VARCHAR(255),
            academic VARCHAR(255) NOT NULL,
            approved BOOLEAN DEFAULT FALSE,
            username VARCHAR(255) NOT NULL
        )
    """)
    db.commit()
except mysql.connector.Error as err:
    logging.error(f"Error: {err}")

@bp.route('/classform', methods=['POST'])
def form():
    cursor = None
    try:
        data = request.json
        logging.debug(f"Dữ liệu nhận được để đăng ký: {data}")

        if not data:
            return jsonify({"error": "Không có dữ liệu nào được cung cấp"}), 400

        object = data.get('object')
        subject = data.get('subject')
        grade = data.get('grade')
        gender = data.get('gender')
        area = data.get('area')
        cond = data.get('cond') if data.get('cond') is not None else ''
        academic = data.get('academic')
        username = data.get('username')

        logging.debug(f"object: {object}, subject: {subject}, grade: {grade}, gender: {gender}, area: {area}, cond: {cond}, academic: {academic}, username: {username}")

        if not all([object, subject, grade, gender, area, academic, username]):
            return jsonify({"error": "Thiếu thông tin trong form"}), 400

        cursor = db.cursor()

        query = """
            INSERT INTO form (object, subject, grade, gender, area, cond, academic, username)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (object, subject, grade, gender, area, cond, academic, username)
        cursor.execute(query, values)
        db.commit()
        response = {'message': 'Thành công rồi, bạn giỏi quá!!!'}
    except mysql.connector.Error as err:
        logging.error(f"Lỗi: {err}")
        response = {'message': f'Lỗi: {err}'}
    finally:
        if cursor:
            cursor.close()
    return jsonify(response)

if db.is_connected():
    print("Kết nối thành công đến cơ sở dữ liệu MySQL.")
else:
    print("Kết nối không thành công đến cơ sở dữ liệu MySQL.")

