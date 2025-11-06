import math
import logging
from typing import Tuple, List, Dict
from app.config import Config

logger = logging.getLogger(__name__)

class NavigationAssistant:
    """Navigation assistant for providing directional guidance"""
    
    def __init__(self, config: Config):
        self.config = config
        self.direction_labels = [
            "center", "front-right", "right", "back-right",
            "back", "back-left", "left", "front-left"
        ]
        
    def calculate_direction(self, center_x: int, center_y: int, frame_width: int, frame_height: int) -> Tuple[str, str]:
        """
        Calculate the direction of an object relative to the camera center
        
        Args:
            center_x: X coordinate of object center
            center_y: Y coordinate of object center
            frame_width: Width of the frame
            frame_height: Height of the frame
            
        Returns:
            Tuple of (direction_label, distance_description)
        """
        # Calculate center of frame
        frame_center_x = frame_width // 2
        frame_center_y = frame_height // 2
        
        # Calculate offset from center
        offset_x = center_x - frame_center_x
        offset_y = center_y - frame_center_y
        
        # Calculate distance from center
        distance = math.sqrt(offset_x**2 + offset_y**2)
        
        # Determine distance description
        if distance < self.config.object_distance_threshold:
            distance_desc = "very close"
        elif distance < self.config.object_distance_threshold * 2:
            distance_desc = "close"
        elif distance < self.config.object_distance_threshold * 4:
            distance_desc = "moderate distance"
        else:
            distance_desc = "far away"
            
        # Handle special case for center
        if abs(offset_x) < self.config.object_distance_threshold and abs(offset_y) < self.config.object_distance_threshold:
            return "center", distance_desc
            
        # Calculate angle in degrees (0° is right, counter-clockwise)
        angle = math.degrees(math.atan2(-offset_y, offset_x))  # Negative y because image coordinates go down
        angle = angle % 360  # Normalize to 0-360
        
        # Divide circle into sectors
        sector_size = 360 / self.config.direction_sectors
        sector_index = int((angle + sector_size / 2) // sector_size) % self.config.direction_sectors
        
        direction_label = self.direction_labels[sector_index]
        
        return direction_label, distance_desc
        
    def get_navigation_instruction(self, detections: List[Dict], frame_width: int, frame_height: int) -> str:
        """
        Generate navigation instruction based on detected objects
        
        Args:
            detections: List of detected objects
            frame_width: Width of the frame
            frame_height: Height of the frame
            
        Returns:
            Navigation instruction
        """
        if not detections:
            return "No objects detected"
            
        # Prioritize person detection for navigation
        persons = [d for d in detections if d['label'] == 'person']
        if persons:
            # Get closest person
            closest_person = min(persons, key=lambda p: 
                                math.sqrt((p['center'][0] - frame_width//2)**2 + 
                                         (p['center'][1] - frame_height//2)**2))
            
            direction, distance = self.calculate_direction(
                closest_person['center'][0],
                closest_person['center'][1],
                frame_width,
                frame_height
            )
            
            if direction == "center":
                return "Person directly ahead"
            else:
                return f"Person detected at {direction}"
                
        # If no persons, prioritize large objects
        largest_object = max(detections, key=lambda d: 
                            (d['bbox'][2] - d['bbox'][0]) * (d['bbox'][3] - d['bbox'][1]))
        
        direction, distance = self.calculate_direction(
            largest_object['center'][0],
            largest_object['center'][1],
            frame_width,
            frame_height
        )
        
        return f"Largest object is {largest_object['label']} at {direction}"