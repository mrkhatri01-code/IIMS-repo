import cv2

class MotionDetector:
    def __init__(self, threshold=30):
        self.threshold = threshold

    def detect_motion(self, video_path, frame_skip=5):
        cap = cv2.VideoCapture(video_path)
        prev_gray = None
        results = []
        frame_idx = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            if frame_idx % frame_skip == 0:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                if prev_gray is not None:
                    diff = cv2.absdiff(prev_gray, gray)
                    motion_score = diff.mean()
                    results.append((frame_idx, motion_score))
                prev_gray = gray
            frame_idx += 1
        cap.release()
        return results 