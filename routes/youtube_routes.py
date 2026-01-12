from flask import Blueprint, request, jsonify, send_from_directory
from services.youtube_service import YouTubeService
from utils.helpers import is_valid_youtube_url
import os

youtube_bp = Blueprint('youtube', __name__, url_prefix='/api/v1/youtube')

@youtube_bp.route('/video_info', methods=['POST'])
def video_info():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({"error": "Missing 'url' parameter in the request body."}), 400

    if not is_valid_youtube_url(url):
        return jsonify({"error": "Invalid YouTube URL."}), 400

    video_info, error_message = YouTubeService.get_video_info(url)

    if video_info:
        return jsonify(video_info), 200
    else:
        return jsonify({"error": error_message}), 500

@youtube_bp.route('/available_resolutions', methods=['POST'])
def available_resolutions():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({"error": "Missing 'url' parameter in the request body."}), 400

    if not is_valid_youtube_url(url):
        return jsonify({"error": "Invalid YouTube URL."}), 400

    resolutions, error_message = YouTubeService.get_available_resolutions(url)

    if resolutions:
        return jsonify(resolutions), 200
    else:
        return jsonify({"error": error_message}), 500

@youtube_bp.route('/available_types/<resolution>', methods=['POST'])
def available_types(resolution):
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({"error": "Missing 'url' parameter in the request body."}), 400

    if not is_valid_youtube_url(url):
        return jsonify({"error": "Invalid YouTube URL."}), 400

    types, error_message = YouTubeService.get_available_types(url, resolution)

    if types:
        return jsonify(types), 200
    else:
        return jsonify({"error": error_message}), 500

@youtube_bp.route('/download/<resolution>', methods=['POST'])
def download_by_resolution(resolution):
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({"error": "Missing 'url' parameter in the request body."}), 400

    if not is_valid_youtube_url(url):
        return jsonify({"error": "Invalid YouTube URL."}), 400

    # Download all types for the resolution
    files = []
    for type in ['full', 'video', 'audio']:
        file_path, filename = YouTubeService.download_and_prepare_file(url, resolution, type)
        if file_path:
            files.append(filename)
        # Note: For 'full' in adaptive, it creates video and audio temp, but we keep them

    if files:
        video_id = url.split('v=')[1].split('&')[0]
        return jsonify({"message": f"Video with resolution {resolution} downloaded successfully.", "files": files, "video_id": video_id}), 200
    else:
        return jsonify({"error": "Failed to download"}), 500

@youtube_bp.route('/download_and_send/<resolution>/<type>', methods=['POST'])
def download_and_send(resolution, type):
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({"error": "Missing 'url' parameter in the request body."}), 400

    if not is_valid_youtube_url(url):
        return jsonify({"error": "Invalid YouTube URL."}), 400

    file_path, filename = YouTubeService.download_and_prepare_file(url, resolution, type)

    if file_path:
        # Send file and schedule cleanup
        response = send_from_directory(os.path.dirname(file_path), filename, as_attachment=True)
        # Note: In production, use a background task to delete file after send
        # For now, keep file
        return response
    else:
        return jsonify({"error": filename}), 404