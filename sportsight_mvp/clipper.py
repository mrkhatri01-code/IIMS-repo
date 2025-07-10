import ffmpeg
import os

def clip_video(input_path, start_time, end_time, output_path):
    (
        ffmpeg
        .input(input_path, ss=start_time, to=end_time)
        .output(output_path, codec='copy')
        .run(overwrite_output=True)
    )

def save_clips(input_path, highlight_segments, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for idx, (start, end) in enumerate(highlight_segments):
        out_path = os.path.join(output_dir, f'clip_{idx+1}.mp4')
        clip_video(input_path, start, end, out_path) 