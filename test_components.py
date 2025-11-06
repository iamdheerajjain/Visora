"""
Test script to verify that all components of the Visora system work correctly
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def test_config():
    """Test configuration loading"""
    print("Testing configuration...")
    try:
        from app.config import Config
        config = Config()
        print(f"✓ Config loaded successfully: {config}")
        return True
    except Exception as e:
        print(f"✗ Config test failed: {e}")
        return False

def test_vision():
    """Test vision module"""
    print("Testing vision module...")
    try:
        from app.config import Config
        from app.vision import ObjectDetector
        config = Config()
        detector = ObjectDetector(config)
        print("✓ Vision module loaded successfully")
        return True
    except Exception as e:
        print(f"✗ Vision module test failed: {e}")
        return False

def test_audio():
    """Test audio module"""
    print("Testing audio module...")
    try:
        from app.config import Config
        from app.audio import AudioManager
        config = Config()
        audio = AudioManager(config)
        print("✓ Audio module loaded successfully")
        return True
    except Exception as e:
        print(f"✗ Audio module test failed: {e}")
        return False

def test_navigation():
    """Test navigation module"""
    print("Testing navigation module...")
    try:
        from app.config import Config
        from app.navigation import NavigationAssistant
        config = Config()
        nav = NavigationAssistant(config)
        print("✓ Navigation module loaded successfully")
        return True
    except Exception as e:
        print(f"✗ Navigation module test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Running Visora component tests...\n")
    
    tests = [
        test_config,
        test_vision,
        test_audio,
        test_navigation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The system is ready to use.")
        return 0
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())