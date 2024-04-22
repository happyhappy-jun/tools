import json
import ffmpeg
import os
import fire
from tqdm import tqdm


def create_output_directory(format):
    output_directory = f"downloaded_{format}s"
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    return output_directory

def configure_ffmpeg(url, output_path, format):
    stream = ffmpeg.input(url)
    if format == 'mp3':
        return ffmpeg.output(stream.audio, output_path, acodec='libmp3lame', ab='192k')
    elif format == 'mp4':
        return ffmpeg.output(stream, output_path, vcodec='copy', acodec='copy')

def process_url(url, title, format, output_directory):
    safe_title = "".join(x for x in title if x.isalnum() or x in " _-").strip()
    output_path = os.path.join(output_directory, f"{safe_title}.{format}")
    output = configure_ffmpeg(url, output_path, format)
    output.run(overwrite_output=True)
    print(f"Downloaded and converted to {format.upper()}: {output_path}")

def download_from_m3u8(json_file, output_format):
    data = json.load(open(json_file, 'r'))
    output_directory = create_output_directory(output_format)
    for entry in tqdm(data):
        for url in entry['m3u8_urls']:
            process_url(url, entry['title'], output_format, output_directory)

def main(json_file, format='mp3'):
    download_from_m3u8(json_file, format)

if __name__ == '__main__':
    fire.Fire(main)
