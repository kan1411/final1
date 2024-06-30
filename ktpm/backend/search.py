from flask import jsonify, request, Blueprint
import mysql.connector
import logging

bp = Blueprint('search', __name__)

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

@bp.route('/register_class', methods=['POST'])
def register_class():
    logging.debug("Received POST request to /register_class")
    data = request.json
    logging.debug(f"Request JSON data: {data}")

    object = data.get('object')
    subject = data.get('subject')
    grade = data.get('grade')
    gender = data.get('gender')
    area = data.get('area')
    username = data.get('username') 

    logging.debug(f"Received data: object={object}, subject={subject}, grade={grade}, gender={gender}, area={area}, username={username}")

    db = get_db_connection()
    if db:
        logging.debug("Database connection successful")
        cursor = db.cursor()
        query = """
            UPDATE form 
            SET registered_by = %s, status = 'Chưa được nhận'
            WHERE object = %s AND subject = %s AND grade = %s AND gender = %s AND area = %s
        """
        logging.debug(f"Executing query: {query} with values ({username}, {object}, {subject}, {grade}, {gender}, {area})")
        cursor.execute(query, (username, object, subject, grade, gender, area))
        db.commit()
        
        rows_affected = cursor.rowcount
        logging.debug(f"Rows affected: {rows_affected}")

        cursor.close()
        db.close()
        
        if rows_affected > 0:
            logging.info("Đã cập nhật dữ liệu thành công.")
            return jsonify({"message": "Đăng ký thành công!"})
        else:
            logging.warning("Không có hàng nào được cập nhật.")
            return jsonify({"message": "Không có hàng nào được cập nhật."}), 400
    else:
        logging.error("Không thể kết nối đến cơ sở dữ liệu.")
        return jsonify({"error": "Không thể kết nối đến cơ sở dữ liệu"}), 500

@bp.route('/get_registered_classes', methods=['GET'])
def get_registered_classes():
    db = get_db_connection()
    if db:
        cursor = db.cursor(dictionary=True)
        query = "SELECT * FROM form WHERE registered_by IS NOT NULL"
        cursor.execute(query)
        registered_classes = cursor.fetchall()
        cursor.close()
        db.close()
        return jsonify(registered_classes)
    else:
        return jsonify({"error": "Không thể kết nối đến cơ sở dữ liệu"}), 500

@bp.route('/students', methods=['GET'])
def get_students():
    object_filter = request.args.get('object', default='', type=str)
    subject_filter = request.args.get('subject', default='', type=str)
    grade_filter = request.args.get('grade', default='', type=str)
    gender_filter = request.args.get('gender', default='', type=str)
    area_filter = request.args.get('area', default='', type=str)

    query = "SELECT * FROM form WHERE approved = 1 AND status = 'Chưa được nhận'"
    filters = []
    
    if object_filter:
        query += " AND object LIKE %s"
        filters.append(f"%{object_filter}%")
    if subject_filter:
        query += " AND subject LIKE %s"
        filters.append(f"%{subject_filter}%")
    if grade_filter:
        query += " AND grade LIKE %s"
        filters.append(f"%{grade_filter}%")
    if gender_filter:
        query += " AND gender LIKE %s"
        filters.append(f"%{gender_filter}%")
    if area_filter:
        query += " AND area LIKE %s"
        filters.append(f"%{area_filter}%")
        
    query += " ORDER BY id DESC"

    db = get_db_connection()
    if db:
        cursor = db.cursor(dictionary=True)
        cursor.execute(query, filters)
        students = cursor.fetchall()
        cursor.close()
        db.close()
        return jsonify(students)
    else:
        return jsonify({"error": "Không thể kết nối đến cơ sở dữ liệu"}), 500

@bp.route('/classinfo', methods=['GET'])
def get_class_info():
    object_filter = request.args.get('object', default='', type=str)
    subject_filter = request.args.get('subject', default='', type=str)
    grade_filter = request.args.get('grade', default='', type=str)
    gender_filter = request.args.get('gender', default='', type=str)
    area_filter = request.args.get('area', default='', type=str)

    query = "SELECT * FROM form WHERE object = %s AND subject = %s AND grade = %s AND gender = %s AND area = %s"
    filters = [object_filter, subject_filter, grade_filter, gender_filter, area_filter]

    db = get_db_connection()
    if db:
        cursor = db.cursor(dictionary=True)
        cursor.execute(query, filters)
        class_info = cursor.fetchone()
        cursor.close()
        db.close()
        if class_info:
            return jsonify(class_info)
        else:
            return jsonify({"error": "Không tìm thấy thông tin lớp học"}), 404
    else:
        return jsonify({"error": "Không thể kết nối đến cơ sở dữ liệu"}), 500
