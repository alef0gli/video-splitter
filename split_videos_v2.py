import os
import subprocess

def get_video_files(directory):
    """Scans the directory for video files."""
    video_extensions = ['.mp4', '.mkv', '.avi', '.mov', '.flv', '.wmv']
    video_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if any(file.lower().endswith(ext) for ext in video_extensions):
                video_files.append(os.path.join(root, file))
    return video_files

def split_video(file_path):
    """Splits the video if its size is greater than 50GB."""
    file_size_gb = os.path.getsize(file_path) / (1024 ** 3)
    if file_size_gb > 50:
        print(f"Splitting video: {file_path}")
        output_path1 = file_path.replace('.', '_part1.')
        output_path2 = file_path.replace('.', '_part2.')
        
        # Get video duration
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        duration = float(result.stdout)
        half_duration = duration / 2

        # Split video into two parts
        subprocess.run(
            ["ffmpeg", "-i", file_path, "-t", str(half_duration), "-c", "copy", output_path1]
        )
        subprocess.run(
            ["ffmpeg", "-i", file_path, "-ss", str(half_duration), "-c", "copy", output_path2]
        )

        print(f"Video split into: {output_path1} and {output_path2}")
    else:
        print(f"Video {file_path} is less than 50GB, no splitting needed.")

def main(directory):
    video_files = get_video_files(directory)
    for video_file in video_files:
        split_video(video_file)

if __name__ == "__main__":
    directory = input("Enter the directory path to scan for videos: ")
    main(directory)
