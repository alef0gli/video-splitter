import os
from moviepy.video.io.VideoFileClip import VideoFileClip

def split_video(file_path, max_size_gb=50):
    try:
        video = VideoFileClip(file_path)
        duration = video.duration
        
        # Split the video into two parts
        midpoint = duration / 2
        first_half = video.subclip(0, midpoint)
        second_half = video.subclip(midpoint, duration)
        
        base_name, ext = os.path.splitext(file_path)
        first_half_file = f"{base_name}_part1{ext}"
        second_half_file = f"{base_name}_part2{ext}"
        
        # Specify codec based on file extension
        if ext.lower() in ['.mp4', '.mov']:
            codec = 'libx264'
        elif ext.lower() == '.webm':
            codec = 'libvpx'
        elif ext.lower() == '.ogv':
            codec = 'libtheora'
        else:
            print(f"Unsupported file format: {ext}")
            return
        
        first_half.write_videofile(first_half_file, codec=codec)
        second_half.write_videofile(second_half_file, codec=codec)
        
        # Close readers to avoid resource warnings
        video.reader.close()
        video.audio.reader.close_proc()
        first_half.reader.close()
        first_half.audio.reader.close_proc()
        second_half.reader.close()
        second_half.audio.reader.close_proc()
        
        print(f"Video split into: {first_half_file} and {second_half_file}")
    except Exception as e:
        print(f"Error splitting video {file_path}: {e}")

def check_videos_in_directory(directory, max_size_gb=50):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if file_path.lower().endswith(('.mp4', '.mkv', '.avi', '.mov', '.webm', '.ogv')):
                file_size_gb = os.path.getsize(file_path) / (1024 * 1024 * 1024)  # Convert bytes to GB
                if file_size_gb > max_size_gb:
                    print(f"Video {file_path} is larger than {max_size_gb}GB. Splitting...")
                    split_video(file_path, max_size_gb)
                else:
                    print(f"Video {file_path} is {file_size_gb:.2f}GB. No need to split.")

if __name__ == "__main__":
    directory = input("Enter the directory path: ")
    check_videos_in_directory(directory)
