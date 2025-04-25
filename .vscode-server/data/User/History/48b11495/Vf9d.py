from flask import Flask, render_template
from models import db

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    
    # Khởi tạo database
    db.init_app(app)
    
    # Đăng ký route
    @app.route('/')
    def index():
        return render_template('index.html')
    
    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)