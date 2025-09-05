#!/usr/bin/env python3
import os
import subprocess
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading
import time

class FFmpegAPIHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/combine':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                audio_file = data.get('audio_file')
                video_file = data.get('video_file')
                output_file = data.get('output_file')
                preset = data.get('preset', 'standard')  # Default to standard preset
                
                if not all([audio_file, video_file, output_file]):
                    self.send_error_response(400, "Missing required parameters: audio_file, video_file, output_file")
                    return
                
                # Validate input files exist
                if not os.path.exists(audio_file):
                    self.send_error_response(400, f"Audio file not found: {audio_file}")
                    return
                if not os.path.exists(video_file):
                    self.send_error_response(400, f"Video file not found: {video_file}")
                    return
                
                # Validate file formats
                audio_error = self.validate_file_format(audio_file, "audio")
                if audio_error:
                    self.send_error_response(400, audio_error)
                    return
                
                video_error = self.validate_file_format(video_file, "video")
                if video_error:
                    self.send_error_response(400, video_error)
                    return
                
                # Build ffmpeg command based on preset
                cmd = self.build_ffmpeg_command(audio_file, video_file, output_file, preset)
                print(f"Executing command: {' '.join(cmd)}")  # Debug logging
                
                try:
                    # Add input handling to prevent hanging
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300, 
                                          stdin=subprocess.DEVNULL)  # 5 minute timeout
                    print(f"FFmpeg completed with return code: {result.returncode}")  # Debug logging
                    
                    if result.returncode == 0:
                        response = {
                            'success': True,
                            'message': 'Files combined successfully',
                            'output_file': output_file,
                            'preset_used': preset,
                            'format': 'MP4 with H.264 video and AAC audio (Instagram/Facebook compatible)'
                        }
                        self.send_json_response(200, response)
                    else:
                        response = {
                            'success': False,
                            'message': 'FFmpeg failed',
                            'error': result.stderr
                        }
                        self.send_json_response(500, response)
                except subprocess.TimeoutExpired:
                    response = {
                        'success': False,
                        'message': 'FFmpeg processing timed out (5 minutes)',
                        'error': 'The video processing took too long and was cancelled'
                    }
                    self.send_json_response(408, response)
                    
            except Exception as e:
                self.send_error_response(500, f"Internal server error: {str(e)}")
        else:
            self.send_error_response(404, "Not found")
    
    def do_GET(self):
        if self.path == '/health':
            self.send_json_response(200, {'status': 'healthy'})
        elif self.path == '/presets':
            presets = {
                'standard': 'Keep original resolution with Instagram/Facebook compatibility',
                'instagram_stories': 'Instagram Stories format (9:16, 1080x1920)',
                'instagram_feed': 'Instagram Feed format (1:1, 1080x1080)',
                'facebook_landscape': 'Facebook Landscape format (16:9, 1280x720)',
                'facebook_square': 'Facebook Square format (1:1, 1080x1080)'
            }
            self.send_json_response(200, {'presets': presets})
        else:
            self.send_error_response(404, "Not found")
    
    def send_json_response(self, status_code, data):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
    
    def send_error_response(self, status_code, message):
        self.send_json_response(status_code, {'success': False, 'error': message})
    
    def validate_file_format(self, file_path, file_type):
        """Validate file format and return error message if invalid"""
        if file_type == "audio":
            # Audio file formats
            if not file_path.lower().endswith(('.mp3', '.aac', '.wav', '.m4a', '.ogg', '.flac')):
                return f"Unsupported {file_type} format. Supported formats: MP3, AAC, WAV, M4A, OGG, FLAC"
        else:
            # Video file formats
            if not file_path.lower().endswith(('.mp4', '.mov', '.avi', '.mkv', '.wmv', '.flv', '.webm')):
                return f"Unsupported {file_type} format. Supported formats: MP4, MOV, AVI, MKV, WMV, FLV, WebM"
        return None
    
    def build_ffmpeg_command(self, audio_file, video_file, output_file, preset):
        """Build ffmpeg command based on preset for Instagram/Facebook compatibility"""
        base_cmd = [
            'ffmpeg', '-y',  # -y to overwrite output files
            '-i', audio_file,
            '-i', video_file,
        ]
        
        # Common settings for Instagram/Facebook compatibility
        common_settings = [
            '-c:v', 'libx264',  # H.264 codec for compatibility
            '-preset', 'medium',  # Balance between speed and quality
            '-profile:v', 'high',  # High profile for better compatibility
            '-level', '4.0',  # Level 4.0 for broad device support
            '-pix_fmt', 'yuv420p',  # YUV 4:2:0 pixel format
            '-c:a', 'aac',  # AAC audio codec
            '-b:a', '128k',  # 128kbps audio bitrate
            '-movflags', '+faststart',  # Move metadata to beginning for faster playback
            '-shortest',  # Match shortest input duration
        ]
        
        # Preset-specific settings
        if preset == 'instagram_stories':
            # Instagram Stories: 9:16 aspect ratio, 1080x1920
            preset_settings = ['-vf', 'scale=1080:1920,setsar=1:1']
        elif preset == 'instagram_feed':
            # Instagram Feed: 1:1 aspect ratio, 1080x1080
            preset_settings = ['-vf', 'scale=1080:1080,setsar=1:1']
        elif preset == 'facebook_landscape':
            # Facebook Landscape: 16:9 aspect ratio, 1280x720
            preset_settings = ['-vf', 'scale=1280:720,setsar=1:1']
        elif preset == 'facebook_square':
            # Facebook Square: 1:1 aspect ratio, 1080x1080
            preset_settings = ['-vf', 'scale=1080:1080,setsar=1:1']
        else:  # 'standard' or any other preset
            # Standard: Keep original resolution but ensure compatibility
            preset_settings = []
        
        return base_cmd + preset_settings + common_settings + [output_file]
    
    def log_message(self, format, *args):
        # Suppress default logging
        pass

def run_server():
    server_address = ('0.0.0.0', 8080)
    httpd = HTTPServer(server_address, FFmpegAPIHandler)
    print(f"FFmpeg API server running on port 8080")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
