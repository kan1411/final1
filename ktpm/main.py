from flask import Flask, send_from_directory
from flask_cors import CORS
import mysql.connector
import logging
from backend.classform import bp as classform_bp
from backend.classinfor import bp as classinfor_bp
from backend.login import bp as login_bp
from backend.personalinfor import bp as personalinfor_bp
from backend.register import bp as register_bp
from backend.search import bp as search_bp
from admin.ad import bp as ad_bp
from admin.admin import bp as admin_bp

app = Flask(__name__)
CORS(app)
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
            app.logger.info("Kết nối thành công đến cơ sở dữ liệu MySQL.")
            return db
    except mysql.connector.Error as err:
        app.logger.error(f"Lỗi kết nối đến cơ sở dữ liệu MySQL: {err}")
        return None

app.register_blueprint(classform_bp)
app.register_blueprint(classinfor_bp)
app.register_blueprint(login_bp)
app.register_blueprint(personalinfor_bp)
app.register_blueprint(register_bp)
app.register_blueprint(search_bp, url_prefix='/api') 
app.register_blueprint(ad_bp, url_prefix='/ad')
app.register_blueprint(admin_bp)

@app.route('/')
def home():
    return send_from_directory('frontend', 'mainpage.html')

@app.route('/<path:path>')
def serve_page(path):
    return send_from_directory('frontend', path)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
