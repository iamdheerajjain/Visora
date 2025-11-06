import os
import platform

# Model configuration
MODEL_NAME = "yolov8n.pt"  # Lightweight YOLOv8 model
CONFIDENCE_THRESHOLD = 0.5
IOU_THRESHOLD = 0.45

# Audio configuration
AUDIO_RATE = 22050
AUDIO_CHUNK = 1024

# Camera configuration
CAMERA_SOURCE = 0  # Default camera
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# Platform-specific camera backend
if platform.system() == "Windows":
    CAMERA_BACKEND = "dshow"  # DirectShow for Windows
else:
    CAMERA_BACKEND = "auto"   # Auto for other platforms

# Navigation configuration
DIRECTION_SECTORS = 8  # Divide 360° into 8 sectors
OBJECT_DISTANCE_THRESHOLD = 50  # Distance threshold in pixels

# Streamlit configuration
STREAMLIT_PORT = 8501
MAX_IMAGE_SIZE = (640, 480)

class Config:
    """Configuration class for the application"""
    
    def __init__(self):
        self.model_name = os.getenv("MODEL_NAME", MODEL_NAME)
        self.confidence_threshold = float(os.getenv("CONFIDENCE_THRESHOLD", CONFIDENCE_THRESHOLD))
        self.iou_threshold = float(os.getenv("IOU_THRESHOLD", IOU_THRESHOLD))
        self.camera_source = int(os.getenv("CAMERA_SOURCE", CAMERA_SOURCE))
        self.camera_backend = os.getenv("CAMERA_BACKEND", CAMERA_BACKEND)
        self.frame_width = int(os.getenv("FRAME_WIDTH", FRAME_WIDTH))
        self.frame_height = int(os.getenv("FRAME_HEIGHT", FRAME_HEIGHT))
        self.direction_sectors = int(os.getenv("DIRECTION_SECTORS", DIRECTION_SECTORS))
        self.object_distance_threshold = int(os.getenv("OBJECT_DISTANCE_THRESHOLD", OBJECT_DISTANCE_THRESHOLD))
        self.streamlit_port = int(os.getenv("STREAMLIT_PORT", STREAMLIT_PORT))
        
    def __str__(self):
        return f"Config(model={self.model_name}, confidence={self.confidence_threshold}, backend={self.camera_backend})"