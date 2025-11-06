import cv2

def test_multiple_cameras():
    """Test multiple camera indices to find an available camera"""
    print("Testing multiple camera indices...")
    
    # Test camera indices 0-3
    for i in range(4):
        print(f"Testing camera index {i}...")
        cap = cv2.VideoCapture(i)
        
        if cap.isOpened():
            print(f"  Camera {i} opened successfully!")
            
            # Try to read a frame
            ret, frame = cap.read()
            
            if ret:
                print(f"  Frame captured successfully! Dimensions: {frame.shape}")
                cap.release()
                print(f"  Camera {i} is working properly!")
                return i  # Return the first working camera index
            else:
                print(f"  Could not read frame from camera {i}")
        else:
            print(f"  Could not open camera {i}")
            
        cap.release()
    
    print("No working cameras found!")
    return None

def test_camera_properties(camera_index=0):
    """Test different camera properties"""
    print(f"Testing camera properties for camera {camera_index}...")
    
    cap = cv2.VideoCapture(camera_index)
    
    if not cap.isOpened():
        print(f"Could not open camera {camera_index}")
        return
    
    # Test different resolutions
    resolutions = [
        (640, 480),
        (1280, 720),
        (1920, 1080)
    ]
    
    for width, height in resolutions:
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        
        actual_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        actual_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        
        ret, frame = cap.read()
        
        if ret:
            print(f"  Resolution {width}x{height}: Supported (actual: {int(actual_width)}x{int(actual_height)})")
        else:
            print(f"  Resolution {width}x{height}: Not supported")
    
    cap.release()

def test_backend_options():
    """Test different camera backends"""
    print("Testing different camera backends...")
    
    backends = [
        (cv2.CAP_DSHOW, "DirectShow"),
        (cv2.CAP_MSMF, "Microsoft Media Foundation"),
        (cv2.CAP_V4L2, "Video4Linux2")
    ]
    
    for backend, name in backends:
        try:
            print(f"Testing {name} backend...")
            cap = cv2.VideoCapture(0, backend)
            
            if cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    print(f"  {name} backend: Working")
                else:
                    print(f"  {name} backend: Opened but can't read frames")
            else:
                print(f"  {name} backend: Could not open")
                
            cap.release()
        except Exception as e:
            print(f"  {name} backend: Error - {e}")

if __name__ == "__main__":
    print("=== Advanced Camera Test ===")
    
    # Test multiple cameras
    working_camera = test_multiple_cameras()
    
    if working_camera is not None:
        # Test properties of working camera
        test_camera_properties(working_camera)
        
        # Test backends
        test_backend_options()
    else:
        print("No cameras found. Please check:")
        print("1. Camera is properly connected")
        print("2. Camera drivers are installed")
        print("3. No other applications are using the camera")
        print("4. Camera permissions are granted")