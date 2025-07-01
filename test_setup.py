#!/usr/bin/env python3
"""
Test script to verify that all dependencies are properly installed
and the face avatar system is ready to run.
"""

import sys
import importlib

def test_imports():
    """Test if all required packages can be imported"""
    required_packages = [
        'cv2',
        'mediapipe',
        'numpy',
        'matplotlib'
    ]
    
    print("Testing package imports...")
    failed_imports = []
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✓ {package} - OK")
        except ImportError as e:
            print(f"✗ {package} - FAILED: {e}")
            failed_imports.append(package)
    
    return len(failed_imports) == 0

def test_camera():
    """Test if camera is accessible"""
    print("\nTesting camera access...")
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            ret, frame = cap.read()
            cap.release()
            if ret:
                print("✓ Camera - OK (can capture frames)")
                return True
            else:
                print("✗ Camera - FAILED (cannot capture frames)")
                return False
        else:
            print("✗ Camera - FAILED (cannot open camera)")
            return False
    except Exception as e:
        print(f"✗ Camera - FAILED: {e}")
        return False

def test_mediapipe():
    """Test MediaPipe face detection"""
    print("\nTesting MediaPipe face detection...")
    try:
        import cv2
        import mediapipe as mp
        import numpy as np
        
        # Initialize MediaPipe
        mp_face_mesh = mp.solutions.face_mesh
        face_mesh = mp_face_mesh.FaceMesh(
            max_num_faces=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Test with a simple image
        test_image = np.zeros((480, 640, 3), dtype=np.uint8)
        rgb_image = cv2.cvtColor(test_image, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_image)
        
        face_mesh.close()
        print("✓ MediaPipe - OK (initialized successfully)")
        return True
        
    except Exception as e:
        print(f"✗ MediaPipe - FAILED: {e}")
        return False

def main():
    """Run all tests"""
    print("Face Avatar Setup Test")
    print("=" * 30)
    
    # Test imports
    imports_ok = test_imports()
    
    # Test camera
    camera_ok = test_camera()
    
    # Test MediaPipe
    mediapipe_ok = test_mediapipe()
    
    print("\n" + "=" * 30)
    print("Test Results:")
    print(f"Package Imports: {'✓ PASS' if imports_ok else '✗ FAIL'}")
    print(f"Camera Access: {'✓ PASS' if camera_ok else '✗ FAIL'}")
    print(f"MediaPipe: {'✓ PASS' if mediapipe_ok else '✗ FAIL'}")
    
    if imports_ok and camera_ok and mediapipe_ok:
        print("\n🎉 All tests passed! Your system is ready to run the face avatar.")
        print("\nTo start the basic avatar:")
        print("  python face_avatar.py")
        print("\nTo start the advanced avatar:")
        print("  python advanced_avatar.py")
    else:
        print("\n❌ Some tests failed. Please check the issues above.")
        if not imports_ok:
            print("\nTo install missing packages:")
            print("  pip install -r requirements.txt")
        if not camera_ok:
            print("\nCamera issues:")
            print("- Make sure your webcam is connected")
            print("- Check if another application is using the camera")
            print("- Try running as administrator (Windows)")

if __name__ == "__main__":
    main() 