import cv2
from ultralytics import YOLO

class YOLOv8Detector:
    def __init__(self, model_name='yolov8n.pt'):
        self.model = YOLO(model_name)

    def detect_in_video(self, video_path, frame_skip=5):
        cap = cv2.VideoCapture(video_path)
        results = []
        frame_idx = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            if frame_idx % frame_skip == 0:
                detections = self.model(frame)
                results.append((frame_idx, detections))
            frame_idx += 1
        cap.release()
        return results 