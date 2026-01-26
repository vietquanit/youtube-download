from pytubefix import YouTube
import subprocess
import os
from utils.helpers import sanitize_filename, extract_video_id, clean_youtube_url

class YouTubeService:
    @staticmethod
    def get_video_info(url):
        try:
            # Sử dụng ANDROID client để tránh lỗi 'Please sign in'
            yt = YouTube(clean_youtube_url(url))
            stream = yt.streams.first()
            video_info = {
                "title": yt.title,
                "author": yt.author,
                "length": yt.length,
                "views": yt.views,
                "description": yt.description,
                "publish_date": yt.publish_date,
            }
            return video_info, None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def get_available_resolutions(url):
        try:
            # Thêm cấu hình để tránh bị YouTube chặn
            yt = YouTube(clean_youtube_url(url),client='WEB_CREATOR')
            print(f"Getting streams for {clean_youtube_url(url)}")
            progressive_resolutions = list(set([
                stream.resolution
                for stream in yt.streams.filter(progressive=True, file_extension='mp4')
                if stream.resolution
            ]))
            all_resolutions = list(set([
                stream.resolution
                for stream in yt.streams.filter(file_extension='mp4')
                if stream.resolution
            ]))
            print(f"Progressive: {progressive_resolutions}, All: {all_resolutions}")
            return {
                "progressive": sorted(progressive_resolutions),
                "all": sorted(all_resolutions)
            }, None
        except Exception as e:
            print(f"Error in get_available_resolutions: {str(e)}")
            return None, str(e)

    @staticmethod
    def get_available_types(url, resolution):
        try:
            yt = YouTube(clean_youtube_url(url))
            # Check if progressive stream exists
            progressive = yt.streams.filter(progressive=True, file_extension='mp4', resolution=resolution).first()
            # Check adaptive
            video = yt.streams.filter(adaptive=True, file_extension='mp4', resolution=resolution, only_video=True).first()
            audio = yt.streams.filter(adaptive=True, file_extension='mp4', only_audio=True).first()

            types = []
            if progressive:
                types.append('full')
            if video and audio:
                types.extend(['video', 'audio', 'full'])
            # Remove duplicates
            types = list(set(types))
            return {"types": types}, None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def download_and_prepare_file(url, resolution, type):
        try:
            yt = YouTube(clean_youtube_url(url))
            title = sanitize_filename(yt.title)
            video_id = extract_video_id(url)
            out_dir = f"./downloads/{video_id}"
            os.makedirs(out_dir, exist_ok=True)

            if type == 'full':
                # Try progressive first
                stream = yt.streams.filter(progressive=True, file_extension='mp4', resolution=resolution).first()
                if stream:
                    filename = f'full_{title}_{resolution}.mp4'
                    file_path = stream.download(output_path=out_dir, filename=filename)
                    return file_path, filename
                else:
                    # Adaptive merge
                    video_stream = yt.streams.filter(adaptive=True, file_extension='mp4', resolution=resolution, only_video=True).first()
                    audio_stream = yt.streams.filter(adaptive=True, file_extension='mp4', only_audio=True).order_by('abr').desc().first()
                    if video_stream and audio_stream:
                        video_file = video_stream.download(output_path=out_dir, filename=f'video_{title}_{resolution}.mp4')
                        audio_file = audio_stream.download(output_path=out_dir, filename=f'audio_{title}_{resolution}.m4a')
                        output_file = os.path.join(out_dir, f'full_{title}_{resolution}.mp4')
                        subprocess.run([
                            'ffmpeg', '-i', video_file, '-i', audio_file,
                            '-c:v', 'copy', '-c:a', 'copy', output_file, '-y'
                        ], check=True)
                        # Clean up temp files
                        os.remove(video_file)
                        os.remove(audio_file)
                        return output_file, f'full_{title}_{resolution}.mp4'
                    else:
                        return None, "Full video not available"
            elif type == 'video':
                video_stream = yt.streams.filter(adaptive=True, file_extension='mp4', resolution=resolution, only_video=True).first()
                if video_stream:
                    filename = f'video_{title}_{resolution}.mp4'
                    file_path = video_stream.download(output_path=out_dir, filename=filename)
                    return file_path, filename
                else:
                    return None, "Video stream not available"
            elif type == 'audio':
                audio_stream = yt.streams.filter(adaptive=True, file_extension='mp4', only_audio=True).order_by('abr').desc().first()
                if audio_stream:
                    filename = f'audio_{title}_{resolution}.m4a'
                    file_path = audio_stream.download(output_path=out_dir, filename=filename)
                    return file_path, filename
                else:
                    return None, "Audio stream not available"
            else:
                return None, "Invalid type"
        except Exception as e:
            return None, str(e)
