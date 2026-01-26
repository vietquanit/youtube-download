from flask import Flask
from flask_cors import CORS
from routes.youtube_routes import youtube_bp
from starlette.middleware.wsgi import WSGIMiddleware

# 1. Khởi tạo Flask
flask_app = Flask(__name__)
CORS(flask_app, resources={r"/api/*": {"origins": "*"}})
flask_app.register_blueprint(youtube_bp)

# 2. Chuyển đổi sang ASGI bằng Starlette để uvicorn chạy được
# Starlette WSGIMiddleware là chuẩn công nghiệp cho việc này
app = WSGIMiddleware(flask_app)

if __name__ == '__main__':
    # Cấu hình fallback nếu chạy bằng: python main.py
    print("--- Flask Dev Server đang chạy tại http://127.0.0.1:8000 ---")
    flask_app.run(debug=True, host='127.0.0.1', port=8000)
