import os
from motion_detector import MotionDetector
from yolov8_detector import YOLOv8Detector
from clipper import save_clips
from commentary_generator import CommentaryGenerator

INPUT_VIDEO = 'sportsight_mvp/input/match.mp4'
CLIPS_DIR = 'sportsight_mvp/output/clips/'
CAPTIONS_DIR = 'sportsight_mvp/output/captions/'

os.makedirs(CLIPS_DIR, exist_ok=True)
os.makedirs(CAPTIONS_DIR, exist_ok=True)

def main():
    print('Detecting motion...')
    motion = MotionDetector()
    motion_scores = motion.detect_motion(INPUT_VIDEO)

    print('Detecting objects...')
    detector = YOLOv8Detector()
    detections = detector.detect_in_video(INPUT_VIDEO)

    # Dummy highlight logic: select top 3 motion spikes
    motion_scores.sort(key=lambda x: x[1], reverse=True)
    highlight_frames = [idx for idx, _ in motion_scores[:3]]
    # Assume each highlight is 5 seconds long, centered on the frame
    import cv2
    cap = cv2.VideoCapture(INPUT_VIDEO)
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()
    highlights = []
    for f in highlight_frames:
        t = f / fps
        start = max(0, t - 2.5)
        end = t + 2.5
        highlights.append((start, end))

    print('Clipping highlights...')
    save_clips(INPUT_VIDEO, highlights, CLIPS_DIR)

    print('Generating commentary...')
    commentator = CommentaryGenerator()
    for i, (start, end) in enumerate(highlights):
        desc = f"Highlight from {start:.1f}s to {end:.1f}s"
        commentary = commentator.generate(desc)
        with open(os.path.join(CAPTIONS_DIR, f'clip_{i+1}.txt'), 'w') as f:
            f.write(commentary)
    print('Done!')

if __name__ == '__main__':
    main() 