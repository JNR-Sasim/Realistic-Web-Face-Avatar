#!/usr/bin/env python3
"""
Simple camera test script to diagnose camera issues
"""

import cv2
import time

def test_camera_index(camera_index, use_dshow=True):
    """Test a specific camera index"""
    print(f"\nTesting camera index {camera_index}...")
    
    try:
        if use_dshow:
            cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
        else:
            cap = cv2.VideoCapture(camera_index)
        
        if not cap.isOpened():
            print(f"✗ Camera {camera_index} failed to open")
            return False
        
        # Try to read a frame
        ret, frame = cap.read()
        if not ret or frame is None:
            print(f"✗ Camera {camera_index} opened but cannot read frames")
            cap.release()
            return False
        
        print(f"✓ Camera {camera_index} working! Frame size: {frame.shape}")
        
        # Show the frame for a few seconds
        print("Showing camera feed for 3 seconds...")
        start_time = time.time()
        
        while time.time() - start_time < 3:
            ret, frame = cap.read()
            if ret:
                cv2.imshow(f'Camera {camera_index}', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break
        
        cv2.destroyAllWindows()
        cap.release()
        return True
        
    except Exception as e:
        print(f"✗ Error with camera {camera_index}: {e}")
        return False

def main():
    """Main test function"""
    print("Camera Test Utility")
    print("=" * 30)
    
    # Test different camera indices with DirectShow
    print("Testing with DirectShow (Windows)...")
    working_cameras = []
    
    for i in range(5):  # Test indices 0-4
        if test_camera_index(i, use_dshow=True):
            working_cameras.append(i)
    
    # If no cameras work with DirectShow, try without
    if not working_cameras:
        print("\nNo cameras found with DirectShow. Trying without...")
        for i in range(5):
            if test_camera_index(i, use_dshow=False):
                working_cameras.append(i)
    
    print("\n" + "=" * 30)
    print("Test Results:")
    
    if working_cameras:
        print(f"✓ Found {len(working_cameras)} working camera(s): {working_cameras}")
        print("\nYou can use any of these camera indices in your avatar application.")
        print("Recommended: Use camera index 0")
    else:
        print("✗ No working cameras found!")
        print("\nTroubleshooting:")
        print("1. Make sure your camera is connected")
        print("2. Check if another application is using the camera")
        print("3. Try running as administrator")
        print("4. Check Windows camera privacy settings")
        print("5. Test your camera in other applications (like Camera app)")
    
    print("\nPress Enter to exit...")
    input()

if __name__ == "__main__":
    main() 