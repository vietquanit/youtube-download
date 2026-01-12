from flask import Flask
from routes.youtube_routes import youtube_bp

app = Flask(__name__)

app.register_blueprint(youtube_bp)

if __name__ == '__main__':
    app.run(debug=True)
