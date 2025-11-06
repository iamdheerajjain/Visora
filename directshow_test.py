import cv2

def test_directshow_backend():
    """Test camera with DirectShow backend specifically"""
    print("Testing camera with DirectShow backend...")
    
    cap = None
    try:
        # Try DirectShow backend specifically (Windows)
        print("Initializing camera with DirectShow backend...")
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        
        if not cap.isOpened():
            print("❌ Could not open camera with DirectShow backend")
            return False
            
        print("✅ Camera opened successfully with DirectShow backend")
        
        # Set properties
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        # Try to read a few frames
        for i in range(5):
            ret, frame = cap.read()
            if ret:
                print(f"✅ Frame {i+1} captured successfully! Shape: {frame.shape}")
            else:
                print(f"❌ Failed to capture frame {i+1}")
                break
                
        # Release camera
        cap.release()
        print("✅ Camera released successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error testing DirectShow backend: {e}")
        if cap:
            cap.release()
        return False

def test_default_backend():
    """Test camera with default backend"""
    print("\nTesting camera with default backend...")
    
    cap = None
    try:
        # Try default backend
        print("Initializing camera with default backend...")
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("❌ Could not open camera with default backend")
            return False
            
        print("✅ Camera opened successfully with default backend")
        
        # Set properties
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        # Try to read a few frames
        for i in range(5):
            ret, frame = cap.read()
            if ret:
                print(f"✅ Frame {i+1} captured successfully! Shape: {frame.shape}")
            else:
                print(f"❌ Failed to capture frame {i+1}")
                break
                
        # Release camera
        cap.release()
        print("✅ Camera released successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error testing default backend: {e}")
        if cap:
            cap.release()
        return False

if __name__ == "__main__":
    print("=== Camera Backend Test ===")
    
    # Test DirectShow backend
    directshow_success = test_directshow_backend()
    
    # Test default backend
    default_success = test_default_backend()
    
    print("\n=== Summary ===")
    print(f"DirectShow backend: {'✅ Working' if directshow_success else '❌ Not working'}")
    print(f"Default backend: {'✅ Working' if default_success else '❌ Not working'}")
    
    if directshow_success or default_success:
        print("\n🎉 Camera is working! You should be able to use it in the Visora application.")
    else:
        print("\n❌ Camera issues detected. Please check:")
        print("1. Camera is properly connected")
        print("2. Camera drivers are installed")
        print("3. No other applications are using the camera")
        print("4. Camera permissions are granted")