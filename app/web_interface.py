import streamlit as st
import cv2
import numpy as np
from PIL import Image
import time
import logging
from app.config import Config
from app.vision import ObjectDetector
from app.audio import AudioManager
from app.navigation import NavigationAssistant

logger = logging.getLogger(__name__)

class WebInterface:
    """Streamlit web interface for the vision assistance system"""
    
    def __init__(self):
        self.config = Config()
        self.detector = None
        self.audio_manager = None
        self.navigation_assistant = None
        self.initialize_components()
        
    def initialize_components(self):
        """Initialize all system components"""
        try:
            self.detector = ObjectDetector(self.config)
            self.audio_manager = AudioManager(self.config)
            self.navigation_assistant = NavigationAssistant(self.config)
            logger.info("All components initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize components: {e}")
            st.error(f"Failed to initialize system components: {e}")
            
    def run(self):
        """Run the Streamlit web application"""
        st.set_page_config(
            page_title="Visora - Vision Assistance for the Blind",
            page_icon="👁️",
            layout="wide"
        )
        
        # Refined CSS with properly applied colors
        st.markdown("""
        <style>
        /* Color definitions */
        .primary-color { color: #2c3e50; }
        .secondary-color { color: #3498db; }
        .accent-color { color: #e74c3c; }
        .success-color { color: #27ae60; }
        .warning-color { color: #f39c12; }
        
        /* Header styling */
        .header {
            text-align: center;
            padding: 2rem;
            background: linear-gradient(135deg, #2c3e50, #1a2530);
            color: white;
            border-radius: 15px;
            margin-bottom: 2rem;
            box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        }
        
        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            font-weight: 700;
        }
        
        .header p {
            font-size: 1.2rem;
            opacity: 0.9;
            max-width: 800px;
            margin: 0 auto;
        }
        
        /* Card styling */
        .feature-card {
            padding: 1.5rem;
            border-radius: 15px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            margin-bottom: 1.5rem;
            background-color: #ffffff;
            border: 1px solid rgba(0,0,0,0.05);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 6px 16px rgba(0,0,0,0.12);
        }
        
        .feature-card h3 {
            color: #2c3e50;
            margin-top: 0;
            border-bottom: 2px solid #3498db;
            padding-bottom: 0.5rem;
        }
        
        /* Detection box */
        .detection-box {
            border: 2px solid #3498db;
            border-radius: 12px;
            padding: 1.2rem;
            margin-top: 1rem;
            background-color: rgba(52, 152, 219, 0.05);
        }
        
        .detection-box h4 {
            color: #3498db;
            margin-top: 0;
        }
        
        /* Announcement styling */
        .announcement {
            background-color: #e1f0fa;
            border-left: 5px solid #3498db;
            padding: 1.2rem;
            margin: 1rem 0;
            border-radius: 0 8px 8px 0;
            color: #2c3e50;
        }
        
        /* Status messages */
        .status-success {
            background-color: #e8f8f5;
            border-left: 5px solid #27ae60;
            padding: 1.2rem;
            margin: 1rem 0;
            border-radius: 0 8px 8px 0;
            color: #2c3e50;
        }
        
        .status-error {
            background-color: #fadbd8;
            border-left: 5px solid #e74c3c;
            padding: 1.2rem;
            margin: 1rem 0;
            border-radius: 0 8px 8px 0;
            color: #2c3e50;
        }
        
        /* Instructions */
        .instructions {
            background-color: #fef9e7;
            border-left: 5px solid #f39c12;
            padding: 1.2rem;
            margin: 1rem 0;
            border-radius: 0 8px 8px 0;
            color: #2c3e50;
        }
        
        /* Button styling */
        .stButton > button {
            background-color: #3498db !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 0.5rem 1rem !important;
            font-weight: 600 !important;
            transition: background-color 0.3s ease !important;
        }
        
        .stButton > button:hover {
            background-color: #2980b9 !important;
        }
        
        /* Sidebar styling */
        [data-testid=stSidebar] {
            background-color: #f8f9fa;
        }
        
        [data-testid=stSidebar] h1, 
        [data-testid=stSidebar] h2, 
        [data-testid=stSidebar] h3 {
            color: #2c3e50;
        }
        
        /* Slider styling */
        .stSlider > div > div > div {
            background-color: #3498db !important;
        }
        
        /* Expander styling */
        .streamlit-expanderHeader {
            background-color: rgba(52, 152, 219, 0.1) !important;
            border-radius: 8px !important;
        }
        
        /* List styling */
        .detection-list {
            padding-left: 1.5rem;
        }
        
        .detection-list li {
            margin-bottom: 0.5rem;
            padding: 0.5rem;
            background-color: rgba(236, 240, 241, 0.5);
            border-radius: 6px;
            list-style-type: none;
        }
        
        /* Responsive design */
        @media (max-width: 768px) {
            .header {
                padding: 1rem;
            }
            
            .header h1 {
                font-size: 1.8rem;
            }
            
            .feature-card {
                padding: 1rem;
            }
        }
        
        /* Custom elements */
        .direction-info {
            padding: 0.5rem;
            background-color: rgba(236, 240, 241, 0.5);
            border-radius: 6px;
            margin: 0.5rem 0;
        }
        
        .object-item {
            background-color: rgba(52, 152, 219, 0.1);
            padding: 0.8rem;
            border-radius: 8px;
            margin-bottom: 0.5rem;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Header with refined design
        st.markdown('''
        <div class="header">
            <h1>👁️ Visora - Vision Assistance System</h1>
            <p>AI-powered computer vision for the visually impaired. Real-time object detection with audio navigation guidance.</p>
        </div>
        ''', unsafe_allow_html=True)
        
        # Introduction card
        st.markdown('''
        <div class="feature-card">
            <h3>About This System</h3>
            <p>This advanced assistive technology uses state-of-the-art computer vision to detect objects in real-time and provides 
            immediate audio feedback to help visually impaired users navigate their environment safely and independently.</p>
            <p><strong>Key Features:</strong></p>
            <ul>
                <li>⚡ Real-time object detection using YOLOv8</li>
                <li>🔊 Immediate audio announcements with directional guidance</li>
                <li>🧭 Smart navigation assistance</li>
                <li>📱 Works with any camera device</li>
            </ul>
        </div>
        ''', unsafe_allow_html=True)
        
        # Sidebar configuration
        with st.sidebar:
            st.header("⚙️ System Configuration")
            confidence_threshold = st.slider(
                "Confidence Threshold",
                0.0, 1.0, self.config.confidence_threshold,
                help="Minimum confidence for object detection"
            )
            
            # Update config
            self.config.confidence_threshold = confidence_threshold
            
            st.markdown("---")
            st.header("🧭 Navigation Guide")
            st.markdown('''
            <div style="background-color: rgba(52, 152, 219, 0.1); padding: 1rem; border-radius: 8px;">
                <p><strong>Directional Terms:</strong></p>
                <ul style="padding-left: 1rem;">
                    <li><strong>Center</strong>: Directly ahead</li>
                    <li><strong>Front-right/Left</strong>: Slightly to the side</li>
                    <li><strong>Right/Left</strong>: To the side</li>
                    <li><strong>Back-right/Left</strong>: Behind and to the side</li>
                    <li><strong>Back</strong>: Directly behind</li>
                </ul>
            </div>
            ''', unsafe_allow_html=True)
            
            st.markdown("---")
            st.header("🔧 Troubleshooting")
            with st.expander("Camera Issues?"):
                st.markdown('''
                1. Ensure no other application is using your camera
                2. Check browser permissions (for web interface)
                3. Try a different camera if available
                4. Restart your computer and try again
                5. Check camera drivers in Device Manager
                ''')
        
        # Camera input section
        st.markdown('''
        <div class="feature-card">
            <h3>📸 Single Image Detection</h3>
            <div class="instructions">
                <strong>How to use:</strong> Click 'Browse files' below to upload an image or use your camera to capture a photo.
            </div>
        ''', unsafe_allow_html=True)
        
        camera_input = st.camera_input("Capture image for object detection", key="camera_input")
        
        if camera_input is not None:
            # Process the image
            self.process_image(camera_input)
            
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Real-time camera section
        st.markdown('''
        <div class="feature-card">
            <h3>🎥 Real-time Object Detection</h3>
            <div class="instructions">
                <strong>How it works:</strong> Real-time object detection starts automatically. 
                Point your camera at objects around you and listen to audio announcements for navigation guidance.
            </div>
        ''', unsafe_allow_html=True)
        
        # Check if components were initialized successfully
        if self.detector is None:
            st.markdown('<div class="status-error">❌ Detector failed to initialize. Cannot start real-time detection.</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            return
            
        # Start real-time detection automatically
        self.run_real_time_detection()
            
        st.markdown('</div>', unsafe_allow_html=True)
            
    def process_image(self, camera_input):
        """Process a single image from camera input"""
        # Check if components were initialized
        if self.detector is None or self.navigation_assistant is None or self.audio_manager is None:
            st.markdown('<div class="status-error">❌ System components not properly initialized.</div>', unsafe_allow_html=True)
            return
            
        try:
            # Convert camera input to OpenCV format
            image = Image.open(camera_input)
            frame = np.array(image)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            
            # Detect objects
            detections = self.detector.detect_objects(frame)
            
            # Draw detections
            annotated_frame = self.detector.draw_detections(frame, detections)
            
            # Convert back to RGB for display
            annotated_frame_rgb = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
            
            # Display the annotated image
            st.image(annotated_frame_rgb, caption="Detected Objects", width='stretch')
            
            # Display detection results
            if detections:
                st.markdown('<div class="detection-box"><h4>Detected Objects:</h4>', unsafe_allow_html=True)
                for i, detection in enumerate(detections):
                    st.markdown(f'''
                    <div class="object-item">
                        <p><strong>{i+1}.</strong> {detection['label']} <em>({detection['confidence']:.2f} confidence)</em></p>
                        <div class="direction-info">
                            <strong>📍 Location:</strong> {detection['center'][0]}, {detection['center'][1]}<br>
                            <strong>Direction:</strong> Calculating...
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
                    
                    # Calculate and announce direction
                    direction, distance = self.navigation_assistant.calculate_direction(
                        detection['center'][0],
                        detection['center'][1],
                        frame.shape[1],
                        frame.shape[0]
                    )
                    
                    # Update the direction info
                    st.markdown(f'''
                    <div style="margin-top: -1.5rem; margin-bottom: 1rem;">
                        <div class="direction-info">
                            <strong>📍 Location:</strong> {direction}, {distance}
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
                    
                    # Announce via audio
                    self.audio_manager.announce_object_direction(
                        detection['label'], direction, distance
                    )
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.info("No objects detected in the image")
                
        except Exception as e:
            logger.error(f"Error processing image: {e}")
            st.markdown(f'<div class="status-error">Error processing image: {e}</div>', unsafe_allow_html=True)
            
    def run_real_time_detection(self):
        """Run real-time object detection using webcam with continuous audio feedback"""
        # Check if components were initialized
        if self.detector is None or self.navigation_assistant is None or self.audio_manager is None:
            st.markdown('<div class="status-error">❌ System components not properly initialized.</div>', unsafe_allow_html=True)
            return
            
        st.markdown('<div class="announcement">🔄 Starting real-time detection...</div>', unsafe_allow_html=True)
        
        # Initialize cap variable
        cap = None
        
        # Create placeholders for video feed and detections
        video_placeholder = st.empty()
        detections_placeholder = st.empty()
        status_placeholder = st.empty()
        
        # Stop button
        stop_button = st.button("⏹️ Stop Detection")
        
        try:
            # Initialize camera with improved error handling
            status_placeholder.markdown('<div class="announcement">🔄 Initializing camera...</div>', unsafe_allow_html=True)
            cap = self.detector.initialize_camera()
            
            # Check if camera opened successfully
            if cap is None:
                status_placeholder.markdown('''
                <div class="status-error">
                    ❌ Could not access the camera. Please check:<br>
                    1. Camera is not being used by another application<br>
                    2. Camera permissions are granted<br>
                    3. Camera drivers are properly installed<br>
                    4. Try a different camera if available
                </div>
                ''', unsafe_allow_html=True)
                return
                
            status_placeholder.markdown('<div class="status-success">✅ Camera connected successfully!</div>', unsafe_allow_html=True)
            
            last_announcement_time = 0
            announcement_interval = 2  # seconds - more frequent announcements
            
            # Track recently announced objects to avoid repetition
            recently_announced = {}
            
            while not stop_button:
                ret, frame = cap.read()
                if not ret:
                    status_placeholder.markdown('<div class="status-error">❌ Failed to read frame from camera</div>', unsafe_allow_html=True)
                    break
                    
                # Detect objects
                detections = self.detector.detect_objects(frame)
                
                # Draw detections
                annotated_frame = self.detector.draw_detections(frame, detections)
                
                # Convert to RGB for display
                annotated_frame_rgb = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
                
                # Display video feed
                video_placeholder.image(annotated_frame_rgb, channels="RGB", width='stretch')
                
                # Process detections for audio feedback
                if detections:
                    detections_html = '''
                    <div class="detection-box">
                        <h4>🎯 Detected Objects:</h4>
                        <div class="detection-list">
                    '''
                    
                    current_time = time.time()
                    
                    # Process each detection for audio feedback
                    for detection in detections[:3]:  # Limit to top 3 detections to avoid audio overload
                        label = detection['label']
                        confidence = detection['confidence']
                        
                        detections_html += f'<div class="object-item"><strong>{label}</strong> ({confidence:.2f})</div>'
                        
                        # Check if we should announce this object
                        should_announce = False
                        
                        # Announce if this is a new object or if enough time has passed since last announcement
                        if label not in recently_announced:
                            should_announce = True
                        elif current_time - recently_announced[label] > 5:  # 5 seconds cooldown
                            should_announce = True
                            
                        if should_announce:
                            # Calculate and announce direction
                            direction, distance = self.navigation_assistant.calculate_direction(
                                detection['center'][0],
                                detection['center'][1],
                                frame.shape[1],
                                frame.shape[0]
                            )
                            
                            # Announce via audio immediately
                            self.audio_manager.announce_object_direction(label, direction, distance)
                            
                            # Update last announcement time
                            recently_announced[label] = current_time
                    
                    detections_html += "</div></div>"
                    detections_placeholder.markdown(detections_html, unsafe_allow_html=True)
                else:
                    detections_placeholder.markdown('<div class="detection-box"><h4>🎯 Detected Objects:</h4><p style="text-align: center; padding: 1rem;">No objects detected</p></div>', unsafe_allow_html=True)
                    
                # Check if stop button was pressed (Streamlit specific)
                # In Streamlit, we need to check the session state
                if 'stop_detection' in st.session_state and st.session_state.stop_detection:
                    break
                    
                # Small delay to prevent excessive CPU usage
                time.sleep(0.05)  # 50ms delay for smoother operation
                
        except Exception as e:
            logger.error(f"Error in real-time detection: {e}")
            st.markdown(f'<div class="status-error">Error in real-time detection: {e}</div>', unsafe_allow_html=True)
        finally:
            if cap is not None:
                cap.release()
                
        st.markdown('<div class="status-success">⏹️ Real-time detection stopped</div>', unsafe_allow_html=True)

def main():
    """Main entry point for the Streamlit app"""
    interface = WebInterface()
    interface.run()

if __name__ == "__main__":
    main()