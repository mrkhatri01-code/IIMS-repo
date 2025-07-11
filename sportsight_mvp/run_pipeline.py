import os
import cv2
import numpy as np
from motion_detector import MotionDetector
from yolov8_detector import YOLOv8Detector
from clipper import save_clips
from commentary_generator import CommentaryGenerator
import random

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
INPUT_VIDEO = os.path.join(current_dir, 'input', 'match.mp4')
CLIPS_DIR = os.path.join(current_dir, 'output', 'clips')
CAPTIONS_DIR = os.path.join(current_dir, 'output', 'captions')

os.makedirs(CLIPS_DIR, exist_ok=True)
os.makedirs(CAPTIONS_DIR, exist_ok=True)

def detect_highlights(motion_scores, fps, threshold_percentile=85):
    """Detect highlight moments based on motion scores"""
    if not motion_scores:
        return []
    
    # Calculate threshold based on percentile
    scores = [score for _, score in motion_scores]
    threshold = np.percentile(scores, threshold_percentile)
    
    # Find frames above threshold
    highlight_frames = []
    for frame_idx, score in motion_scores:
        if score > threshold:
            highlight_frames.append(frame_idx)
    
    # Group consecutive frames into segments
    if not highlight_frames:
        return []
    
    segments = []
    start_frame = highlight_frames[0]
    prev_frame = start_frame
    
    for frame in highlight_frames[1:]:
        if frame - prev_frame > 30:  # Gap of more than 30 frames (1 second at 30fps)
            # End current segment
            segments.append((start_frame, prev_frame))
            start_frame = frame
        prev_frame = frame
    
    # Add final segment
    segments.append((start_frame, prev_frame))
    
    # Convert to time segments (10-15 seconds each, centered on the segment)
    highlights = []
    for start_frame, end_frame in segments[:5]:  # Limit to top 5 highlights
        center_time = (start_frame + end_frame) / 2 / fps
        clip_length = random.uniform(10, 15)  # 10 to 15 seconds
        start_time = max(0, center_time - clip_length / 2)
        end_time = center_time + clip_length / 2
        highlights.append((start_time, end_time))
    
    return highlights

def main():
    print('🎬 SportSight MVP - AI Sports Highlight Generator')
    print('=' * 50)
    
    if not os.path.exists(INPUT_VIDEO):
        print(f"❌ Error: Input video not found at {INPUT_VIDEO}")
        return
    
    print('📹 Detecting motion...')
    motion = MotionDetector(threshold=25)
    motion_scores = motion.detect_motion(INPUT_VIDEO)
    
    if not motion_scores:
        print("❌ No motion detected in video")
        return

    print('🔍 Detecting objects...')
    detector = YOLOv8Detector()
    detections = detector.detect_in_video(INPUT_VIDEO)

    # Get video properties
    cap = cv2.VideoCapture(INPUT_VIDEO)
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps
    cap.release()
    
    print(f'📊 Video info: {duration:.1f}s, {fps:.1f} fps, {total_frames} frames')

    # Detect highlights using improved algorithm
    highlights = detect_highlights(motion_scores, fps)
    
    if not highlights:
        print("❌ No highlights detected")
        return
    
    print(f'🎯 Found {len(highlights)} highlight segments')

    print('✂️  Clipping highlights...')
    try:
        save_clips(INPUT_VIDEO, highlights, CLIPS_DIR)
        print(f'✅ Clips saved to {CLIPS_DIR}')
    except Exception as e:
        print(f'❌ Error clipping videos: {e}')
        return

    print('🎤 Generating commentary...')
    commentator = CommentaryGenerator()
    for i, (start, end) in enumerate(highlights):
        desc = f"Sports highlight from {start:.1f}s to {end:.1f}s - intense action moment"
        commentary = commentator.generate(desc)
        
        caption_file = os.path.join(CAPTIONS_DIR, f'clip_{i+1}.txt')
        with open(caption_file, 'w') as f:
            f.write(f"Highlight {i+1}\n")
            f.write(f"Time: {start:.1f}s - {end:.1f}s\n")
            f.write(f"Duration: {end-start:.1f}s\n")
            f.write("-" * 40 + "\n")
            f.write(commentary)
        
        print(f'📝 Commentary saved: clip_{i+1}.txt')
    
    print('🎉 Pipeline completed successfully!')
    print(f'📁 Check {CLIPS_DIR} for video clips')
    print(f'📁 Check {CAPTIONS_DIR} for commentary files')

if __name__ == '__main__':
    main() 