# SportSight MVP

## Objective
Detect highlight-worthy moments in a sports video using motion tracking and object detection, automatically clip those moments, and generate AI-based natural language commentary.

## Features
- **Object Detection:** YOLOv8 (Ultralytics)
- **Motion Tracking:** OpenCV (frame differencing)
- **Highlight Clipping:** FFmpeg (via ffmpeg-python)
- **Commentary Generation:** GPT-4.1 (Azure OpenAI) or MatchTime GPT-2 (HuggingFace)

## Folder Structure
```
sportsight_mvp/
├── input/
│   └── match.mp4
├── output/
│   ├── clips/
│   └── captions/
├── yolov8_detector.py
├── motion_detector.py
├── clipper.py
├── commentary_generator.py
├── run_pipeline.py
├── .env
├── requirements.txt
└── README.md
```

## Setup
1. **Clone the repo and install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Configure API keys:**
   - Copy `.env.example` to `.env` and fill in your Azure OpenAI or HuggingFace credentials.
3. **Place your input video:**
   - Put your `match.mp4` in the `input/` folder.

## Usage
```bash
python run_pipeline.py
```

- Highlight clips will be saved in `output/clips/`
- Commentary text files will be saved in `output/captions/`

## Requirements
- Python 3.8+
- See `requirements.txt` for package list

## Notes
- For MVP, action classification is dummy logic.
- Either Azure OpenAI or HuggingFace can be used for commentary. 