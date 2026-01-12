## Description
The YouTube Video Downloader and Info API is a Flask-based Python project that allows you to download YouTube videos and retrieve video information using Pytube. This versatile tool provides functionalities for downloading videos in various resolutions and types.

## Features
- Download YouTube videos in various resolutions and types (full, video, audio).
- Retrieve comprehensive information about YouTube videos.
- Modular structure for easy extension (e.g., adding Facebook support).
- Error handling for reliable performance.
- JSON API endpoints for easy integration.

## Project Structure
```
BE/
├── main.py                 # Main application entry point
├── services/
│   └── youtube_service.py  # YouTube-specific business logic
├── routes/
│   └── youtube_routes.py   # API routes for YouTube
├── utils/
│   └── helpers.py          # Utility functions (validation, sanitization)
├── downloads/              # Temporary download directory
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## Libraries and Technologies Used
- Python 3.x
- Flask for building the API.
- Pytube for interacting with YouTube content.
- FFmpeg for merging video/audio streams.

## Installation
1. Clone or download this repository.
2. Install Python dependencies: `pip install -r requirements.txt`
3. **Install FFmpeg** (required for merging video and audio streams):
   - Download from [FFmpeg official site](https://ffmpeg.org/download.html).
   - Choose "Windows builds" (e.g., from gyan.dev or BtbN).
   - Download the ZIP file, extract to a folder (e.g., `C:\ffmpeg`).
   - Add `C:\ffmpeg\bin` to your system's PATH environment variable:
     - Search for "Environment Variables" in Windows search.
     - Edit "Path" in System variables, add the bin path.
     - Restart your terminal/VS Code.
   - Verify: Run `ffmpeg -version` in terminal.
4. Run the app: `python main.py`

## API Endpoints

All endpoints are prefixed with `/api/v1/youtube`.

### Get Video Info
- **Endpoint:** `/api/v1/youtube/video_info`
- **Method:** POST
- **Body:** `{"url": "https://www.youtube.com/watch?v=VIDEO_ID"}`
- **Response:** Video details (title, author, etc.)

### Get Available Resolutions
- **Endpoint:** `/api/v1/youtube/available_resolutions`
- **Method:** POST
- **Body:** `{"url": "https://www.youtube.com/watch?v=VIDEO_ID"}`
- **Response:** `{"progressive": [...], "all": [...]}`

### Get Available Types for Resolution
- **Endpoint:** `/api/v1/youtube/available_types/<resolution>`
- **Method:** POST
- **Body:** `{"url": "https://www.youtube.com/watch?v=VIDEO_ID"}`
- **Response:** `{"types": ["full", "video", "audio"]}` (depending on resolution)

### Download to Server
- **Endpoint:** `/api/v1/youtube/download/<resolution>`
- **Method:** POST
- **Body:** `{"url": "https://www.youtube.com/watch?v=VIDEO_ID"}`
- **Response:** `{"message": "...", "files": [...], "video_id": "..."}`

### Download and Send File Directly
- **Endpoint:** `/api/v1/youtube/download_and_send/<resolution>/<type>`
- **Method:** POST
- **Body:** `{"url": "https://www.youtube.com/watch?v=VIDEO_ID"}`
- **Response:** File download (browser will prompt save)
- **Type:** `full`, `video`, `audio`

## Handling Multiple Clients
To prevent server overload:
- Files are stored temporarily in `downloads/` directory.
- Implement cleanup: Delete files after download or use a scheduler (e.g., APScheduler) to remove old files.
- For production, consider:
  - Rate limiting (e.g., Flask-Limiter).
  - Queue system (e.g., Celery) for downloads.
  - Cloud storage for files instead of local disk.
  - Streaming downloads without saving to disk (advanced).

## Future Extensions
- Add Facebook video download support in `services/facebook_service.py` and `routes/facebook_routes.py`.
- Update blueprints in `main.py`.
