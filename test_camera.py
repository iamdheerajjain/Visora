import cv2

def test_camera():
    """Test if camera is accessible"""
    print("Testing camera access...")
    
    # Try to open the default camera (index 0)
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("ERROR: Could not open camera. Please check:")
        print("1. Camera is not being used by another application")
        print("2. Camera permissions are granted to your browser/Python")
        print("3. Camera drivers are properly installed")
        return False
    
    print("Camera opened successfully!")
    
    # Try to read a frame
    ret, frame = cap.read()
    
    if not ret:
        print("ERROR: Could not read frame from camera")
        cap.release()
        return False
    
    print(f"Frame captured successfully! Dimensions: {frame.shape}")
    
    # Release the camera
    cap.release()
    print("Camera test completed successfully!")
    return True

if __name__ == "__main__":
    test_camera()