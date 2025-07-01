import cv2
import mediapipe as mp
import numpy as np
import time

class RealisticFaceAvatar:
    def __init__(self):
        # Initialize MediaPipe
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        # Initialize face mesh with 3D mesh enabled
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
        self.avatar_size = 500
        self.face_landmarks = None
        self.prev_landmarks = None
        
        # Performance tracking
        self.fps_counter = 0
        self.fps_start_time = time.time()
        self.current_fps = 0
        
        # Smoothing
        self.smoothing_factor = 0.7
        self.smoothed_landmarks = None
        
    def initialize_camera(self):
        """Initialize camera with multiple attempts and different indices"""
        camera_indices = [0, 1, 2]
        
        for camera_index in camera_indices:
            try:
                print(f"Trying camera index {camera_index}...")
                self.cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
                
                if self.cap.isOpened():
                    self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                    self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                    self.cap.set(cv2.CAP_PROP_FPS, 30)
                    
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
        
        raise RuntimeError("No camera could be initialized.")
    
    def get_face_landmarks(self, frame):
        """Extract face landmarks from frame"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)
        
        if results.multi_face_landmarks:
            landmarks = results.multi_face_landmarks[0]
            return landmarks
        return None
    
    def smooth_landmarks(self, landmarks):
        """Apply smoothing to reduce jitter"""
        if landmarks is None:
            return None
            
        if self.smoothed_landmarks is None:
            self.smoothed_landmarks = landmarks
            return landmarks
        
        # Smooth landmark positions
        for i, landmark in enumerate(landmarks.landmark):
            smoothed_landmark = self.smoothed_landmarks.landmark[i]
            landmark.x = landmark.x * (1 - self.smoothing_factor) + smoothed_landmark.x * self.smoothing_factor
            landmark.y = landmark.y * (1 - self.smoothing_factor) + smoothed_landmark.y * self.smoothing_factor
            landmark.z = landmark.z * (1 - self.smoothing_factor) + smoothed_landmark.z * self.smoothing_factor
        
        self.smoothed_landmarks = landmarks
        return landmarks
    
    def draw_realistic_avatar(self, landmarks, frame):
        """Draw a realistic avatar using MediaPipe's 3D face mesh"""
        if landmarks is None:
            return frame
        
        h, w, _ = frame.shape
        
        # Create avatar canvas
        avatar = np.zeros((self.avatar_size, self.avatar_size, 3), dtype=np.uint8)
        avatar[:] = (30, 30, 30)  # Dark background
        
        # Get all 468 landmarks in 3D
        landmark_points = []
        for landmark in landmarks.landmark:
            x = int(landmark.x * w)
            y = int(landmark.y * h)
            z = landmark.z  # 3D depth information
            landmark_points.append((x, y, z))
        
        # Create realistic face mesh using MediaPipe's face mesh connections
        self.draw_face_mesh_realistic(avatar, landmark_points, w, h)
        
        # Add avatar to frame
        avatar_resized = cv2.resize(avatar, (300, 300))
        frame[10:310, 10:310] = avatar_resized
        
        return frame
    
    def draw_face_mesh_realistic(self, avatar, landmark_points, w, h):
        """Draw realistic face mesh using MediaPipe's face mesh connections"""
        # MediaPipe face mesh connections for realistic face
        face_mesh_connections = [
            # Face outline
            (10, 338), (338, 297), (297, 332), (332, 284), (284, 251), (251, 389), (389, 356), (356, 454), (454, 323), (323, 361), (361, 288), (288, 397), (397, 365), (365, 379), (379, 378), (378, 400), (400, 377), (377, 152), (152, 148), (148, 176), (176, 149), (149, 150), (150, 136), (136, 172), (172, 58), (58, 132), (132, 93), (93, 234), (234, 127), (127, 162), (162, 21), (21, 54), (54, 103), (103, 67), (67, 109), (109, 10),
            
            # Left eye
            (33, 7), (7, 163), (163, 144), (144, 145), (145, 153), (153, 154), (154, 155), (155, 133), (133, 173), (173, 157), (157, 158), (158, 159), (159, 160), (160, 161), (161, 246), (246, 33),
            
            # Right eye
            (362, 382), (382, 381), (381, 380), (380, 374), (374, 373), (373, 390), (390, 249), (249, 263), (263, 466), (466, 388), (388, 387), (387, 386), (386, 385), (385, 384), (384, 398), (398, 362),
            
            # Nose
            (1, 2), (2, 98), (98, 97), (97, 2), (2, 326), (326, 327), (327, 2), (2, 165), (165, 164), (164, 0), (0, 37), (37, 39), (39, 40), (40, 185), (185, 61), (61, 146), (146, 91), (91, 181), (181, 84), (84, 17), (17, 314), (314, 405), (405, 320), (320, 307), (307, 375), (375, 321), (321, 308), (308, 324), (324, 318), (318, 78), (78, 95), (95, 88), (88, 178), (178, 87), (87, 14), (14, 317), (317, 402), (402, 318), (318, 324), (324, 308), (308, 415), (415, 310), (310, 311), (311, 312), (312, 13), (13, 82), (82, 81), (81, 80), (80, 191), (191, 78), (78, 95), (95, 88), (88, 178), (178, 87), (87, 14), (14, 317), (317, 402), (402, 318), (318, 324), (324, 308), (308, 415), (415, 310), (310, 311), (311, 312), (312, 13), (13, 82), (82, 81), (81, 80), (80, 191), (191, 78),
            
            # Mouth
            (61, 84), (84, 17), (17, 314), (314, 405), (405, 320), (320, 307), (307, 375), (375, 321), (321, 308), (308, 324), (324, 318), (318, 78), (78, 95), (95, 88), (88, 178), (178, 87), (87, 14), (14, 317), (317, 402), (402, 318), (318, 324), (324, 308), (308, 415), (415, 310), (310, 311), (311, 312), (312, 13), (13, 82), (82, 81), (81, 80), (80, 191), (191, 78),
            
            # Eyebrows
            (70, 63), (63, 105), (105, 66), (66, 107), (107, 55), (55, 65), (65, 52), (52, 53), (53, 46), (46, 70), (300, 293), (293, 334), (334, 296), (296, 336), (336, 285), (285, 295), (295, 282), (282, 283), (283, 276), (276, 300)
        ]
        
        # Scale and center landmarks for avatar
        scaled_points = self.scale_and_center_landmarks(landmark_points, self.avatar_size)
        
        # Draw face mesh connections
        for connection in face_mesh_connections:
            start_idx, end_idx = connection
            if start_idx < len(scaled_points) and end_idx < len(scaled_points):
                start_point = scaled_points[start_idx]
                end_point = scaled_points[end_idx]
                
                # Draw line with depth-based color
                color = self.get_depth_color(landmark_points[start_idx][2], landmark_points[end_idx][2])
                cv2.line(avatar, start_point, end_point, color, 1)
        
        # Fill face areas with realistic colors
        self.fill_face_areas(avatar, scaled_points, landmark_points)
    
    def get_depth_color(self, z1, z2):
        """Get color based on depth (z-coordinate)"""
        # Normalize depth to color (closer = brighter)
        depth = (z1 + z2) / 2
        intensity = int(255 * (1 - abs(depth)))
        return (intensity, intensity, intensity)
    
    def fill_face_areas(self, avatar, scaled_points, landmark_points):
        """Fill face areas with realistic colors"""
        # Face outline points
        face_outline_indices = [10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288, 397, 365, 379, 378, 400, 377, 152, 148, 176, 149, 150, 136, 172, 58, 132, 93, 234, 127, 162, 21, 54, 103, 67, 109]
        
        if len(face_outline_indices) > 0:
            face_points = []
            for idx in face_outline_indices:
                if idx < len(scaled_points):
                    face_points.append(scaled_points[idx])
            
            if len(face_points) > 2:
                face_points = np.array(face_points, dtype=np.int32)
                cv2.fillPoly(avatar, [face_points], (255, 200, 150))  # Skin color
        
        # Eyes
        left_eye_indices = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
        right_eye_indices = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
        
        # Fill left eye
        if len(left_eye_indices) > 0:
            left_eye_points = []
            for idx in left_eye_indices:
                if idx < len(scaled_points):
                    left_eye_points.append(scaled_points[idx])
            
            if len(left_eye_points) > 2:
                left_eye_points = np.array(left_eye_points, dtype=np.int32)
                cv2.fillPoly(avatar, [left_eye_points], (255, 255, 255))  # White
        
        # Fill right eye
        if len(right_eye_indices) > 0:
            right_eye_points = []
            for idx in right_eye_indices:
                if idx < len(scaled_points):
                    right_eye_points.append(scaled_points[idx])
            
            if len(right_eye_points) > 2:
                right_eye_points = np.array(right_eye_points, dtype=np.int32)
                cv2.fillPoly(avatar, [right_eye_points], (255, 255, 255))  # White
        
        # Mouth
        mouth_indices = [61, 84, 17, 314, 405, 320, 307, 375, 321, 308, 324, 318]
        
        if len(mouth_indices) > 0:
            mouth_points = []
            for idx in mouth_indices:
                if idx < len(scaled_points):
                    mouth_points.append(scaled_points[idx])
            
            if len(mouth_points) > 2:
                mouth_points = np.array(mouth_points, dtype=np.int32)
                cv2.fillPoly(avatar, [mouth_points], (150, 50, 50))  # Red
    
    def scale_and_center_landmarks(self, landmark_points, target_size):
        """Scale and center landmarks to fit in target size"""
        if len(landmark_points) == 0:
            return []
        
        # Extract x, y coordinates
        points_2d = [(point[0], point[1]) for point in landmark_points]
        points_2d = np.array(points_2d)
        
        # Get bounding box
        min_x, min_y = points_2d.min(axis=0)
        max_x, max_y = points_2d.max(axis=0)
        
        # Calculate scale
        scale_x = (target_size * 0.8) / (max_x - min_x) if max_x > min_x else 1
        scale_y = (target_size * 0.8) / (max_y - min_y) if max_y > min_y else 1
        scale = min(scale_x, scale_y)
        
        # Scale and center
        scaled_points = []
        for point in points_2d:
            scaled_x = int((point[0] - min_x) * scale + target_size * 0.1)
            scaled_y = int((point[1] - min_y) * scale + target_size * 0.1)
            scaled_points.append((scaled_x, scaled_y))
        
        return scaled_points
    
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
        """Add information text to frame"""
        cv2.putText(frame, f"FPS: {self.current_fps}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        status = "Face Detected" if self.face_landmarks else "No Face"
        color = (0, 255, 0) if self.face_landmarks else (0, 0, 255)
        cv2.putText(frame, status, (10, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        
        cv2.putText(frame, "Realistic 3D Face Mesh", (10, 90), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        
        cv2.putText(frame, "Press 'q' to quit", (10, 120), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    def run(self):
        """Main loop for realistic face avatar"""
        print("Starting Realistic Face Avatar (3D Mesh)...")
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
                
                # Apply smoothing
                if self.face_landmarks:
                    self.face_landmarks = self.smooth_landmarks(self.face_landmarks)
                
                # Draw landmarks on frame
                frame = self.draw_landmarks_on_frame(frame, self.face_landmarks)
                
                # Draw realistic avatar
                frame = self.draw_realistic_avatar(self.face_landmarks, frame)
                
                # Calculate and display FPS
                self.calculate_fps()
                self.add_info_text(frame)
                
                # Display frame
                cv2.imshow('Realistic Face Avatar (3D Mesh)', frame)
                
                # Check for quit
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                    
        except KeyboardInterrupt:
            print("\nStopping Realistic Face Avatar...")
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
    avatar = RealisticFaceAvatar()
    try:
        avatar.run()
    except Exception as e:
        print(f"Failed to start avatar: {e}")
        print("\nTroubleshooting tips:")
        print("1. Close other applications that might be using the camera")
        print("2. Try running as administrator")
        print("3. Check if your camera is working in other applications")
        print("4. Restart your computer if the issue persists") 