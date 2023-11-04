import requests
import os
import subprocess
import argparse
from urllib.parse import urljoin

def download_m3u8_video(m3u8_url, output_file):
    # Create a temporary directory to store video segments
    temp_dir = 'temp_video_segments'
    os.makedirs(temp_dir, exist_ok=True)

    # Fetch the M3U8 playlist
    response = requests.get(m3u8_url)
    if response.status_code != 200:
        print("Failed to fetch M3U8 playlist.")
        return

    # Parse the M3U8 playlist and download video segments
    lines = response.text.split('\n')
    segment_urls = [urljoin(m3u8_url, line.strip()) for line in lines if line and not line.startswith('#')]
    for i, segment_url in enumerate(segment_urls):
        segment_filename = os.path.join(temp_dir, f'segment_{i}.ts')
        response = requests.get(segment_url)
        with open(segment_filename, 'wb') as segment_file:
            segment_file.write(response.content)

    # Use ffmpeg to concatenate the video segments into the final video file
    cmd = ['ffmpeg', '-i', f'concat:{"|".join([f"{temp_dir}/segment_{i}.ts" for i in range(len(segment_urls))])}', '-c', 'copy', output_file]
    subprocess.run(cmd)

    # Clean up temporary directory
    for i in range(len(segment_urls)):
        os.remove(f'{temp_dir}/segment_{i}.ts')
    os.rmdir(temp_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download a video from an M3U8 playlist.")
    parser.add_argument("m3u8_url", help="M3U8 video URL")
    parser.add_argument("output_file", help="Output video file name")

    args = parser.parse_args()

    download_m3u8_video(args.m3u8_url, args.output_file)
    print("Video download complete.")
