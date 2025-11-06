"""
Main entry point for the Visora vision assistance system.
This system helps visually impaired users navigate their environment
using real-time object detection and audio guidance.
"""

import logging
import argparse
from app.config import Config
from app.vision import ObjectDetector
from app.audio import AudioManager
from app.navigation import NavigationAssistant

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main function to run the vision assistance system"""
    parser = argparse.ArgumentParser(description="Visora - Vision Assistance System")
    parser.add_argument(
        "--mode",
        choices=["web", "cli"],
        default="web",
        help="Run mode: web (Streamlit interface) or cli (command line)"
    )
    
    args = parser.parse_args()
    
    try:
        logger.info("Starting Visora vision assistance system")
        config = Config()
        
        if args.mode == "web":
            # Import and run web interface
            from app.web_interface import main as web_main
            web_main()
        else:
            # Run CLI version
            run_cli_version(config)
            
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
    except Exception as e:
        logger.error(f"Application error: {e}")
        raise

def run_cli_version(config: Config):
    """Run the command-line version of the application"""
    logger.info("Running CLI version of the application")
    
    # Initialize components
    detector = ObjectDetector(config)
    audio_manager = AudioManager(config)
    navigation_assistant = NavigationAssistant(config)
    
    logger.info("System components initialized")
    logger.info("Starting camera feed...")
    
    # Initialize camera
    import cv2
    cap = cv2.VideoCapture(config.camera_source)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.frame_height)
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                logger.error("Failed to read frame from camera")
                break
                
            # Detect objects
            detections = detector.detect_objects(frame)
            
            # Draw detections on frame
            annotated_frame = detector.draw_detections(frame, detections)
            
            # Display frame (optional)
            cv2.imshow("Visora - Vision Assistance", annotated_frame)
            
            # Provide audio guidance
            if detections:
                # Get navigation instruction
                instruction = navigation_assistant.get_navigation_instruction(
                    detections, frame.shape[1], frame.shape[0]
                )
                
                # Announce via audio
                audio_manager.announce_navigation(instruction)
                
                # Print to console
                print(f"Navigation: {instruction}")
                
            # Break on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    except Exception as e:
        logger.error(f"Error in CLI mode: {e}")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        logger.info("Application shutdown complete")

if __name__ == "__main__":
    main()