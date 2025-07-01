import cv2
import mediapipe as mp
import numpy as np
import math
from collections import deque

class AdvancedFaceAvatar:
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
        
        # Initialize camera
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        
        # Avatar parameters
        self.avatar_size = 400
        self.face_landmarks = None
        self.prev_landmarks = None
        
        # Expression tracking
        self.expression_history = deque(maxlen=10)
        self.current_expression = "neutral"
        
        # Performance tracking
        self.fps_counter = 0
        self.fps_start_time = time.time()
        self.current_fps = 0
        
        # Smoothing
        self.smoothing_factor = 0.7
        self.smoothed_landmarks = None
        
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
    
    def detect_expression(self, landmarks):
        """Detect facial expression based on landmark positions"""
        if landmarks is None:
            return "neutral"
        
        # Get key landmark indices
        left_eye_top = 159
        left_eye_bottom = 145
        right_eye_top = 386
        right_eye_bottom = 374
        mouth_top = 13
        mouth_bottom = 14
        left_eyebrow = 70
        right_eyebrow = 300
        
        # Calculate eye openness
        left_eye_openness = abs(landmarks.landmark[left_eye_top].y - landmarks.landmark[left_eye_bottom].y)
        right_eye_openness = abs(landmarks.landmark[right_eye_top].y - landmarks.landmark[right_eye_bottom].y)
        avg_eye_openness = (left_eye_openness + right_eye_openness) / 2
        
        # Calculate mouth openness
        mouth_openness = abs(landmarks.landmark[mouth_top].y - landmarks.landmark[mouth_bottom].y)
        
        # Calculate eyebrow position
        eyebrow_height = (landmarks.landmark[left_eyebrow].y + landmarks.landmark[right_eyebrow].y) / 2
        
        # Determine expression
        if avg_eye_openness < 0.02:  # Eyes very closed
            expression = "sleepy"
        elif mouth_openness > 0.05:  # Mouth open
            expression = "surprised"
        elif eyebrow_height < 0.3:  # Eyebrows raised
            expression = "surprised"
        elif mouth_openness < 0.01:  # Mouth very closed
            expression = "serious"
        else:
            expression = "neutral"
        
        self.expression_history.append(expression)
        
        # Get most common expression in history
        if len(self.expression_history) > 0:
            self.current_expression = max(set(self.expression_history), key=self.expression_history.count)
        
        return self.current_expression
    
    def draw_advanced_avatar(self, landmarks, frame):
        """Draw an advanced avatar with better features"""
        if landmarks is None:
            return frame
        
        h, w, _ = frame.shape
        
        # Create avatar canvas
        avatar = np.zeros((self.avatar_size, self.avatar_size, 3), dtype=np.uint8)
        avatar[:] = (30, 30, 30)  # Dark background
        
        # Extract facial features
        face_outline = self.get_face_outline(landmarks, w, h)
        left_eye = self.get_eye_landmarks(landmarks, w, h, "left")
        right_eye = self.get_eye_landmarks(landmarks, w, h, "right")
        mouth = self.get_mouth_landmarks(landmarks, w, h)
        eyebrows = self.get_eyebrow_landmarks(landmarks, w, h)
        
        # Draw face outline
        if len(face_outline) > 0:
            face_outline = self.scale_and_center_points(face_outline, self.avatar_size)
            cv2.fillPoly(avatar, [face_outline], (255, 200, 150))  # Skin color
        
        # Draw eyebrows
        if len(eyebrows) > 0:
            eyebrows = self.scale_and_center_points(eyebrows, self.avatar_size)
            cv2.fillPoly(avatar, [eyebrows], (100, 50, 0))  # Brown
        
        # Draw eyes with pupils
        if len(left_eye) > 0:
            left_eye = self.scale_and_center_points(left_eye, self.avatar_size)
            cv2.fillPoly(avatar, [left_eye], (255, 255, 255))  # White
            # Add pupil
            eye_center = np.mean(left_eye, axis=0).astype(int)
            cv2.circle(avatar, tuple(eye_center), 8, (0, 0, 0), -1)  # Black pupil
        
        if len(right_eye) > 0:
            right_eye = self.scale_and_center_points(right_eye, self.avatar_size)
            cv2.fillPoly(avatar, [right_eye], (255, 255, 255))  # White
            # Add pupil
            eye_center = np.mean(right_eye, axis=0).astype(int)
            cv2.circle(avatar, tuple(eye_center), 8, (0, 0, 0), -1)  # Black pupil
        
        # Draw mouth with expression
        if len(mouth) > 0:
            mouth = self.scale_and_center_points(mouth, self.avatar_size)
            mouth_color = self.get_expression_color()
            cv2.fillPoly(avatar, [mouth], mouth_color)
        
        # Add expression text
        cv2.putText(avatar, self.current_expression.upper(), 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        
        # Add avatar to frame
        avatar_resized = cv2.resize(avatar, (250, 250))
        frame[10:260, 10:260] = avatar_resized
        
        return frame
    
    def get_face_outline(self, landmarks, w, h):
        """Get face outline landmarks"""
        face_indices = [10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288, 
                       397, 365, 379, 378, 400, 377, 152, 148, 176, 149, 150, 136, 
                       172, 58, 132, 93, 234, 127, 162, 21, 54, 103, 67, 109]
        
        points = []
        for i in face_indices:
            landmark = landmarks.landmark[i]
            x = int(landmark.x * w)
            y = int(landmark.y * h)
            points.append((x, y))
        
        return np.array(points)
    
    def get_eye_landmarks(self, landmarks, w, h, eye_side):
        """Get eye landmarks for left or right eye"""
        if eye_side == "left":
            eye_indices = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
        else:
            eye_indices = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
        
        points = []
        for i in eye_indices:
            landmark = landmarks.landmark[i]
            x = int(landmark.x * w)
            y = int(landmark.y * h)
            points.append((x, y))
        
        return np.array(points)
    
    def get_mouth_landmarks(self, landmarks, w, h):
        """Get mouth landmarks"""
        mouth_indices = [61, 84, 17, 314, 405, 320, 307, 375, 321, 308, 324, 318]
        
        points = []
        for i in mouth_indices:
            landmark = landmarks.landmark[i]
            x = int(landmark.x * w)
            y = int(landmark.y * h)
            points.append((x, y))
        
        return np.array(points)
    
    def get_eyebrow_landmarks(self, landmarks, w, h):
        """Get eyebrow landmarks"""
        eyebrow_indices = [70, 63, 105, 66, 107, 55, 65, 52, 53, 46, 300, 293, 334, 296, 336, 285, 295, 282, 283, 276]
        
        points = []
        for i in eyebrow_indices:
            landmark = landmarks.landmark[i]
            x = int(landmark.x * w)
            y = int(landmark.y * h)
            points.append((x, y))
        
        return np.array(points)
    
    def get_expression_color(self):
        """Get color based on current expression"""
        colors = {
            "neutral": (150, 50, 50),
            "happy": (50, 150, 50),
            "surprised": (50, 50, 150),
            "serious": (100, 100, 100),
            "sleepy": (150, 150, 50)
        }
        return colors.get(self.current_expression, (150, 50, 50))
    
    def scale_and_center_points(self, points, target_size):
        """Scale and center points to fit in target size"""
        if len(points) == 0:
            return points
        
        min_x, min_y = points.min(axis=0)
        max_x, max_y = points.max(axis=0)
        
        scale_x = (target_size * 0.8) / (max_x - min_x) if max_x > min_x else 1
        scale_y = (target_size * 0.8) / (max_y - min_y) if max_y > min_y else 1
        scale = min(scale_x, scale_y)
        
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
        """Add information text to frame"""
        cv2.putText(frame, f"FPS: {self.current_fps}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        status = "Face Detected" if self.face_landmarks else "No Face"
        color = (0, 255, 0) if self.face_landmarks else (0, 0, 255)
        cv2.putText(frame, status, (10, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        
        cv2.putText(frame, f"Expression: {self.current_expression}", (10, 90), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        
        cv2.putText(frame, "Press 'q' to quit", (10, 120), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    def run(self):
        """Main loop for advanced face avatar"""
        print("Starting Advanced Face Avatar...")
        print("Press 'q' to quit")
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to grab frame")
                break
            
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Get face landmarks
            self.face_landmarks = self.get_face_landmarks(frame)
            
            # Apply smoothing
            if self.face_landmarks:
                self.face_landmarks = self.smooth_landmarks(self.face_landmarks)
                
                # Detect expression
                self.detect_expression(self.face_landmarks)
            
            # Draw landmarks on frame
            frame = self.draw_landmarks_on_frame(frame, self.face_landmarks)
            
            # Draw advanced avatar
            frame = self.draw_advanced_avatar(self.face_landmarks, frame)
            
            # Calculate and display FPS
            self.calculate_fps()
            self.add_info_text(frame)
            
            # Display frame
            cv2.imshow('Advanced Face Avatar', frame)
            
            # Check for quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        self.cap.release()
        cv2.destroyAllWindows()
        self.face_mesh.close()

if __name__ == "__main__":
    import time
    avatar = AdvancedFaceAvatar()
    try:
        avatar.run()
    except KeyboardInterrupt:
        print("\nStopping Advanced Face Avatar...")
        avatar.cleanup() 