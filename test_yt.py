from pytubefix import YouTube
try:
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ" # Never Gonna Give You Up
    yt = YouTube(url)
    print(f"Title: {yt.title}")
    resolutions = [s.resolution for s in yt.streams.filter(file_extension='mp4') if s.resolution]
    print(f"Resolutions: {list(set(resolutions))}")
except Exception as e:
    print(f"FAILED: {e}")
