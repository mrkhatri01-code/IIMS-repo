import cv2
import numpy as np

class MotionDetector:
    def __init__(self, threshold=25):
        self.threshold = threshold

    def detect_motion(self, video_path, frame_skip=3):
        """Detect motion in video using frame differencing with improved scoring"""
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Error: Could not open video {video_path}")
            return []
        
        prev_gray = None
        results = []
        frame_idx = 0
        
        print("Processing video frames for motion detection...")
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
                
            if frame_idx % frame_skip == 0:
                # Convert to grayscale and apply Gaussian blur to reduce noise
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                gray = cv2.GaussianBlur(gray, (21, 21), 0)
                
                if prev_gray is not None:
                    # Calculate frame difference
                    diff = cv2.absdiff(prev_gray, gray)
                    
                    # Apply threshold to get binary image
                    thresh = cv2.threshold(diff, self.threshold, 255, cv2.THRESH_BINARY)[1]
                    
                    # Calculate motion score based on percentage of changed pixels
                    motion_pixels = np.sum(thresh > 0)
                    total_pixels = thresh.shape[0] * thresh.shape[1]
                    motion_score = (motion_pixels / total_pixels) * 100
                    
                    # Add some smoothing to avoid noise
                    if motion_score > 0.1:  # Only record significant motion
                        results.append((frame_idx, motion_score))
                
                prev_gray = gray
            
            frame_idx += 1
            
            # Progress indicator
            if frame_idx % 100 == 0:
                print(f"Processed {frame_idx} frames...")
        
        cap.release()
        print(f"Motion detection completed. Found {len(results)} motion events.")
        return results 