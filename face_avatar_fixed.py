import cv2
import mediapipe as mp
import numpy as np
import time
import sys

class FaceAvatarFixed:
    def __init__(self):
        # Initialize MediaPipe
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        # Initialize face mesh with optimized settings
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Initialize camera with better error handling
        self.cap = None
        self.initialize_camera()
        
        # Avatar parameters
        self.avatar_size = 300
        self.face_landmarks = None
        self.prev_landmarks = None
        
        # Performance tracking
        self.fps_counter = 0
        self.fps_start_time = time.time()
        self.current_fps = 0
        
    def initialize_camera(self):
        """Initialize camera with multiple attempts and different indices"""
        camera_indices = [0, 1, 2]  # Try different camera indices
        
        for camera_index in camera_indices:
            try:
                print(f"Trying camera index {camera_index}...")
                self.cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)  # Use DirectShow on Windows
                
                if self.cap.isOpened():
                    # Set camera properties
                    self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                    self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                    self.cap.set(cv2.CAP_PROP_FPS, 30)
                    
                    # Test if we can actually read a frame
                    ret, frame = self.cap.read()
                    if ret and frame is not None:
                        print(f"✓ Camera {camera_index} initialized successfully!")
                        return
                    else:
                        print(f"✗ Camera {camera_index} opened but cannot read frames")
                        self.cap.release()
                        self.cap = None
                else:
                    print(f"✗ Camera {camera_index} failed to open")
                    
            except Exception as e:
                print(f"✗ Error with camera {camera_index}: {e}")
                if self.cap:
                    self.cap.release()
                    self.cap = None
        
        # If no camera works, try without DirectShow
        print("Trying without DirectShow...")
        try:
            self.cap = cv2.VideoCapture(0)
            if self.cap.isOpened():
                ret, frame = self.cap.read()
                if ret and frame is not None:
                    print("✓ Camera initialized without DirectShow!")
                    return
                else:
                    self.cap.release()
                    self.cap = None
        except Exception as e:
            print(f"Error without DirectShow: {e}")
        
        raise RuntimeError("No camera could be initialized. Please check if your camera is connected and not being used by another application.")
    
    def get_face_landmarks(self, frame):
        """Extract face landmarks from frame"""
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame
        results = self.face_mesh.process(rgb_frame)
        
        if results.multi_face_landmarks:
            landmarks = results.multi_face_landmarks[0]
            return landmarks
        return None
    
    def draw_avatar(self, landmarks, frame):
        """Draw a simple avatar based on face landmarks"""
        if landmarks is None:
            return frame
        
        # Get frame dimensions
        h, w, _ = frame.shape
        
        # Create avatar canvas
        avatar = np.zeros((self.avatar_size, self.avatar_size, 3), dtype=np.uint8)
        avatar[:] = (50, 50, 50)  # Dark background
        
        # Extract key facial features
        face_points = []
        eye_left_points = []
        eye_right_points = []
        mouth_points = []
        
        for i, landmark in enumerate(landmarks.landmark):
            x = int(landmark.x * w)
            y = int(landmark.y * h)
            
            # Face outline (oval)
            if i in [10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288, 397, 365, 379, 378, 400, 377, 152, 148, 176, 149, 150, 136, 172, 58, 132, 93, 234, 127, 162, 21, 54, 103, 67, 109]:
                face_points.append((x, y))
            
            # Left eye
            if i in [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]:
                eye_left_points.append((x, y))
            
            # Right eye
            if i in [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]:
                eye_right_points.append((x, y))
            
            # Mouth
            if i in [61, 84, 17, 314, 405, 320, 307, 375, 321, 308, 324, 318]:
                mouth_points.append((x, y))
        
        # Draw face outline on avatar
        if len(face_points) > 0:
            face_points = np.array(face_points)
            # Scale and center face points
            face_points = self.scale_and_center_points(face_points, self.avatar_size)
            cv2.fillPoly(avatar, [face_points], (255, 200, 150))  # Skin color
        
        # Draw eyes
        if len(eye_left_points) > 0:
            eye_left_points = np.array(eye_left_points)
            eye_left_points = self.scale_and_center_points(eye_left_points, self.avatar_size)
            cv2.fillPoly(avatar, [eye_left_points], (255, 255, 255))  # White
        
        if len(eye_right_points) > 0:
            eye_right_points = np.array(eye_right_points)
            eye_right_points = self.scale_and_center_points(eye_right_points, self.avatar_size)
            cv2.fillPoly(avatar, [eye_right_points], (255, 255, 255))  # White
        
        # Draw mouth
        if len(mouth_points) > 0:
            mouth_points = np.array(mouth_points)
            mouth_points = self.scale_and_center_points(mouth_points, self.avatar_size)
            cv2.fillPoly(avatar, [mouth_points], (150, 50, 50))  # Red
        
        # Add avatar to frame
        avatar_resized = cv2.resize(avatar, (200, 200))
        frame[10:210, 10:210] = avatar_resized
        
        return frame
    
    def scale_and_center_points(self, points, target_size):
        """Scale and center points to fit in target size"""
        if len(points) == 0:
            return points
        
        # Get bounding box
        min_x, min_y = points.min(axis=0)
        max_x, max_y = points.max(axis=0)
        
        # Calculate scale
        scale_x = (target_size * 0.8) / (max_x - min_x) if max_x > min_x else 1
        scale_y = (target_size * 0.8) / (max_y - min_y) if max_y > min_y else 1
        scale = min(scale_x, scale_y)
        
        # Scale and center
        scaled_points = (points - np.array([min_x, min_y])) * scale
        centered_points = scaled_points + np.array([target_size * 0.1, target_size * 0.1])
        
        return centered_points.astype(np.int32)
    
    def draw_landmarks_on_frame(self, frame, landmarks):
        """Draw MediaPipe landmarks on frame"""
        if landmarks:
            self.mp_drawing.draw_landmarks(
                image=frame,
                landmark_list=landmarks,
                connections=self.mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=self.mp_drawing_styles.get_default_face_mesh_tesselation_style()
            )
        return frame
    
    def calculate_fps(self):
        """Calculate current FPS"""
        self.fps_counter += 1
        if time.time() - self.fps_start_time >= 1.0:
            self.current_fps = self.fps_counter
            self.fps_counter = 0
            self.fps_start_time = time.time()
    
    def add_info_text(self, frame):
        """Add FPS and status information to frame"""
        cv2.putText(frame, f"FPS: {self.current_fps}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        status = "Face Detected" if self.face_landmarks else "No Face"
        color = (0, 255, 0) if self.face_landmarks else (0, 0, 255)
        cv2.putText(frame, status, (10, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        
        cv2.putText(frame, "Press 'q' to quit", (10, 90), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    def run(self):
        """Main loop for face avatar"""
        print("Starting Face Avatar (Fixed Version)...")
        print("Press 'q' to quit")
        
        try:
            while True:
                if self.cap is None or not self.cap.isOpened():
                    print("Camera connection lost. Attempting to reconnect...")
                    self.initialize_camera()
                    continue
                
                ret, frame = self.cap.read()
                if not ret or frame is None:
                    print("Failed to read frame. Attempting to reconnect...")
                    self.cap.release()
                    self.initialize_camera()
                    continue
                
                # Flip frame horizontally for mirror effect
                frame = cv2.flip(frame, 1)
                
                # Get face landmarks
                self.face_landmarks = self.get_face_landmarks(frame)
                
                # Draw landmarks on frame
                frame = self.draw_landmarks_on_frame(frame, self.face_landmarks)
                
                # Draw avatar
                frame = self.draw_avatar(self.face_landmarks, frame)
                
                # Calculate and display FPS
                self.calculate_fps()
                self.add_info_text(frame)
                
                # Display frame
                cv2.imshow('Face Avatar (Fixed)', frame)
                
                # Check for quit
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                    
        except KeyboardInterrupt:
            print("\nStopping Face Avatar...")
        except Exception as e:
            print(f"Error during execution: {e}")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        self.face_mesh.close()

if __name__ == "__main__":
    avatar = FaceAvatarFixed()
    try:
        avatar.run()
    except Exception as e:
        print(f"Failed to start avatar: {e}")
        print("\nTroubleshooting tips:")
        print("1. Close other applications that might be using the camera")
        print("2. Try running as administrator")
        print("3. Check if your camera is working in other applications")
        print("4. Restart your computer if the issue persists") 