import cv2
import numpy as np
from ultralytics import YOLO
import logging
from typing import List, Tuple, Dict, Optional
from app.config import Config

logger = logging.getLogger(__name__)

class ObjectDetector:
    """YOLO-based object detector for real-time object detection"""
    
    def __init__(self, config: Config):
        self.config = config
        self.model = None
        self.class_names = []
        self._load_model()
        
    def _load_model(self):
        """Load the YOLO model"""
        try:
            logger.info(f"Loading YOLO model: {self.config.model_name}")
            self.model = YOLO(self.config.model_name)
            # Get class names from the model
            if hasattr(self.model, 'names'):
                self.class_names = self.model.names
            else:
                # Default COCO class names
                self.class_names = [
                    'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train',
                    'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign',
                    'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep',
                    'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella',
                    'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard',
                    'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard',
                    'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup', 'fork',
                    'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange',
                    'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair',
                    'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv',
                    'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave',
                    'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase',
                    'scissors', 'teddy bear', 'hair drier', 'toothbrush'
                ]
            logger.info("Model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise
            
    def _get_backend_code(self):
        """Get OpenCV backend code based on configuration"""
        backend_map = {
            "dshow": cv2.CAP_DSHOW,
            "msmf": cv2.CAP_MSMF,
            "v4l2": cv2.CAP_V4L2,
            "auto": None
        }
        return backend_map.get(self.config.camera_backend, None)
            
    def initialize_camera(self, camera_source=None) -> Optional[cv2.VideoCapture]:
        """
        Initialize camera with better error handling and backend selection
        
        Args:
            camera_source: Camera source index (default from config)
            
        Returns:
            cv2.VideoCapture object or None if failed
        """
        if camera_source is None:
            camera_source = self.config.camera_source
            
        # Try configured backend first
        backends_to_try = []
        backend_code = self._get_backend_code()
        
        if backend_code is not None:
            backends_to_try.append(backend_code)
            
        # Add other common backends as fallbacks
        backends_to_try.extend([
            cv2.CAP_DSHOW,    # DirectShow (Windows)
            cv2.CAP_MSMF,     # Microsoft Media Foundation (Windows)
            -1                # Auto detection
        ])
        
        # Remove duplicates while preserving order
        seen = set()
        unique_backends = []
        for backend in backends_to_try:
            if backend not in seen:
                seen.add(backend)
                unique_backends.append(backend)
        
        for backend in unique_backends:
            cap = None
            try:
                logger.info(f"Trying to initialize camera {camera_source} with backend {backend}")
                
                if backend == -1:
                    cap = cv2.VideoCapture(camera_source)
                else:
                    cap = cv2.VideoCapture(camera_source, backend)
                
                if cap.isOpened():
                    # Set frame properties
                    cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.config.frame_width)
                    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config.frame_height)
                    
                    # Test if we can read a frame
                    ret, frame = cap.read()
                    if ret:
                        logger.info(f"Camera initialized successfully with backend {backend}")
                        return cap
                    else:
                        logger.warning(f"Camera opened but could not read frame with backend {backend}")
                        cap.release()
                        cap = None
                else:
                    logger.warning(f"Could not open camera with backend {backend}")
                    if cap:
                        cap.release()
                        cap = None
                    
            except Exception as e:
                logger.error(f"Error initializing camera with backend {backend}: {e}")
                if cap:
                    cap.release()
                    cap = None
                    
        logger.error("Failed to initialize camera with all backends")
        return None
            
    def detect_objects(self, frame: np.ndarray) -> List[Dict]:
        """
        Detect objects in a frame
        
        Args:
            frame: Input image frame
            
        Returns:
            List of detected objects with bounding boxes and labels
        """
        if self.model is None:
            raise RuntimeError("Model not loaded")
            
        try:
            # Run object detection
            results = self.model(
                frame,
                conf=self.config.confidence_threshold,
                iou=self.config.iou_threshold
            )
            
            detections = []
            if results and len(results) > 0:
                result = results[0]
                boxes = result.boxes
                
                if boxes is not None:
                    for i in range(len(boxes)):
                        box = boxes.xyxy[i].cpu().numpy().astype(int)
                        confidence = float(boxes.conf[i].cpu().numpy())
                        class_id = int(boxes.cls[i].cpu().numpy())
                        
                        # Calculate center point
                        center_x = int((box[0] + box[2]) / 2)
                        center_y = int((box[1] + box[3]) / 2)
                        
                        detection = {
                            'bbox': box.tolist(),
                            'center': (center_x, center_y),
                            'confidence': confidence,
                            'class_id': class_id,
                            'label': self.class_names[class_id] if class_id < len(self.class_names) else f"Class {class_id}"
                        }
                        detections.append(detection)
                        
            return detections
        except Exception as e:
            logger.error(f"Detection failed: {e}")
            return []
            
    def draw_detections(self, frame: np.ndarray, detections: List[Dict]) -> np.ndarray:
        """
        Draw bounding boxes and labels on the frame
        
        Args:
            frame: Input image frame
            detections: List of detected objects
            
        Returns:
            Frame with drawn detections
        """
        annotated_frame = frame.copy()
        
        for detection in detections:
            bbox = detection['bbox']
            label = detection['label']
            confidence = detection['confidence']
            center = detection['center']
            
            # Draw bounding box
            cv2.rectangle(
                annotated_frame,
                (bbox[0], bbox[1]),
                (bbox[2], bbox[3]),
                (0, 255, 0),
                2
            )
            
            # Draw label
            label_text = f"{label} {confidence:.2f}"
            cv2.putText(
                annotated_frame,
                label_text,
                (bbox[0], bbox[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2
            )
            
            # Draw center point
            cv2.circle(annotated_frame, center, 5, (0, 0, 255), -1)
            
        return annotated_frame