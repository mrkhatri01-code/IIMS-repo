import ffmpeg
import os
import subprocess

def clip_video(input_path, start_time, end_time, output_path):
    """Clip video using ffmpeg with error handling"""
    try:
        # Use ffmpeg-python for clipping
        (
            ffmpeg
            .input(input_path, ss=start_time, to=end_time)
            .output(output_path, codec='copy', acodec='copy')
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True, quiet=True)
        )
        return True
    except ffmpeg.Error as e:
        print(f"FFmpeg error: {e.stderr.decode() if e.stderr else str(e)}")
        return False
    except Exception as e:
        print(f"Error clipping video: {e}")
        return False

def save_clips(input_path, highlight_segments, output_dir):
    """Save multiple video clips with progress tracking"""
    os.makedirs(output_dir, exist_ok=True)
    
    successful_clips = 0
    total_clips = len(highlight_segments)
    
    for idx, (start, end) in enumerate(highlight_segments):
        out_path = os.path.join(output_dir, f'clip_{idx+1}.mp4')
        
        print(f"  Creating clip {idx+1}/{total_clips}: {start:.1f}s - {end:.1f}s")
        
        if clip_video(input_path, start, end, out_path):
            successful_clips += 1
            print(f"  ✅ Clip {idx+1} saved: {out_path}")
        else:
            print(f"  ❌ Failed to create clip {idx+1}")
    
    print(f"📊 Clipping complete: {successful_clips}/{total_clips} clips created successfully")
    return successful_clips 