from flask import Flask, jsonify, request, send_from_directory, Blueprint
import mysql.connector
import logging

bp = Blueprint('admin', __name__)

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
        logging.error(f"Error connecting to MySQL: {err}")
        return None

@bp.route('/users', methods=['GET'])
def get_users():
    cursor = None
    db = get_db_connection()
    if not db:
        return jsonify({"message": "MySQL Connection not available."}), 500

    try:
        cursor = db.cursor(dictionary=True)
        query = "SELECT id, username, name, gender, role, area, phone, academic FROM users"
        cursor.execute(query)
        users = cursor.fetchall()
        logging.debug(f"Users fetched: {users}")
        return jsonify(users)
    except mysql.connector.Error as err:
        logging.error(f"Lỗi khi lấy danh sách người dùng: {err}")
        return jsonify({'message': f'Lỗi khi lấy danh sách người dùng: {err}'}), 500
    finally:
        if cursor:
            cursor.close()
        db.close()

@bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    cursor = None
    db = get_db_connection()
    if not db:
        return jsonify({"message": "MySQL Connection not available."}), 500

    try:
        cursor = db.cursor()
        query = "DELETE FROM users WHERE id = %s"
        cursor.execute(query, (user_id,))
        db.commit()
        logging.debug(f"User with id {user_id} deleted successfully.")
        return jsonify({'message': 'Người dùng đã bị xóa thành công!'})
    except mysql.connector.Error as err:
        logging.error(f"Lỗi khi xóa người dùng: {err}")
        return jsonify({'message': f'Lỗi khi xóa người dùng: {err}'}), 500
    finally:
        if cursor:
            cursor.close()
        db.close()

@bp.route('/forms', methods=['GET'])
def get_forms():
    cursor = None
    db = get_db_connection()
    if not db:
        return jsonify({"message": "MySQL Connection not available."}), 500

    try:
        cursor = db.cursor(dictionary=True)
        query = "SELECT * FROM form WHERE approved = FALSE"
        cursor.execute(query)
        forms = cursor.fetchall()
        logging.debug(f"Forms fetched: {forms}")
        return jsonify(forms)
    except mysql.connector.Error as err:
        logging.error(f"Lỗi khi lấy danh sách form: {err}")
        return jsonify({'message': f'Lỗi khi lấy danh sách form: {err}'}), 500
    finally:
        if cursor:
            cursor.close()
        db.close()

@bp.route('/forms/<int:form_id>/approve', methods=['POST'])
def approve_form(form_id):
    cursor = None
    db = get_db_connection()
    if not db:
        return jsonify({"message": "MySQL Connection not available."}), 500

    try:
        cursor = db.cursor()
        query = "UPDATE form SET approved = TRUE WHERE id = %s"
        cursor.execute(query, (form_id,))
        db.commit()
        logging.debug(f"Form with id {form_id} approved successfully.")
        return jsonify({'message': 'Form đã được duyệt thành công!'})
    except mysql.connector.Error as err:
        logging.error(f"Lỗi khi duyệt form: {err}")
        return jsonify({'message': f'Lỗi khi duyệt form: {err}'}), 500
    finally:
        if cursor:
            cursor.close()
        db.close()

@bp.route('/forms/<int:form_id>', methods=['DELETE'])
def delete_form(form_id):
    cursor = None
    db = get_db_connection()
    if not db:
        return jsonify({"message": "MySQL Connection not available."}), 500

    try:
        cursor = db.cursor()
        query = "DELETE FROM form WHERE id = %s"
        cursor.execute(query, (form_id,))
        db.commit()
        logging.debug(f"Form with id {form_id} deleted successfully.")
        return jsonify({'message': 'Form đã bị xóa thành công!'})
    except mysql.connector.Error as err:
        logging.error(f"Lỗi khi xóa form: {err}")
        return jsonify({'message': f'Lỗi khi xóa form: {err}'}), 500
    finally:
        if cursor:
            cursor.close()
        db.close()
