"""
Face Mesh Detector Module
Uses OpenCV for face detection and landmark extraction.
Compatible with Python 3.13+
"""

import cv2
import numpy as np
from typing import Optional, List, Tuple
import os


class FaceMeshDetector:
    """
    Detects and tracks facial landmarks using OpenCV.

    Compatible with Python 3.13+ (alternative to MediaPipe).
    Generates synthetic landmarks from face detection for biometric features.
    """

    def __init__(self,
                 static_image_mode: bool = False,
                 max_num_faces: int = 1,
                 refine_landmarks: bool = True,
                 min_detection_confidence: float = 0.5,
                 min_tracking_confidence: float = 0.5):
        """
        Initialize the Face detector.

        Args:
            static_image_mode: Whether to treat input as static images
            max_num_faces: Maximum number of faces to detect
            refine_landmarks: Whether to refine landmarks (compatibility parameter)
            min_detection_confidence: Minimum confidence for face detection
            min_tracking_confidence: Minimum confidence for tracking (compatibility parameter)
        """
        self.static_image_mode = static_image_mode
        self.max_num_faces = max_num_faces
        self.refine_landmarks = refine_landmarks
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence

        # Initialize OpenCV face detector (Haar Cascade)
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(cascade_path)

        # Initialize eye detector for more detailed landmarks
        eye_cascade_path = cv2.data.haarcascades + 'haarcascade_eye.xml'
        self.eye_cascade = cv2.CascadeClassifier(eye_cascade_path)
        
    def detect(self, image: np.ndarray) -> Optional[List[np.ndarray]]:
        """
        Detect facial landmarks in an image.

        Args:
            image: Input image in BGR format (OpenCV format)

        Returns:
            List of landmark arrays for each detected face, or None if no face detected.
            Each landmark array has shape (468, 3) containing (x, y, z) coordinates.
        """
        h, w = image.shape[:2]
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

        if len(faces) == 0:
            return None

        # Limit to max_num_faces
        faces = faces[:self.max_num_faces]

        # Generate landmarks for each detected face
        all_landmarks = []

        for (x, y, fw, fh) in faces:
            # Generate synthetic landmarks from face region
            landmarks = self._generate_landmarks(image, gray, x, y, fw, fh)
            all_landmarks.append(landmarks)

        return all_landmarks

    def _generate_landmarks(self, image, gray, x, y, fw, fh):
        """
        Generate synthetic landmarks from face region.
        Creates 468 landmarks to match MediaPipe format.
        """
        landmarks = np.zeros((468, 3))

        # Detect eyes within face region
        face_roi = gray[y:y+fh, x:x+fw]
        eyes = self.eye_cascade.detectMultiScale(face_roi, 1.1, 5)

        # Define key facial points based on face geometry
        center_x = x + fw // 2
        center_y = y + fh // 2

        # Generate landmarks in a face-like pattern
        idx = 0

        # Face contour (0-16): Jaw line
        for i in range(17):
            ratio = i / 16.0
            lx = x + fw * ratio
            ly = y + fh * (0.8 + 0.2 * np.sin(ratio * np.pi))
            landmarks[idx] = [lx, ly, 0]
            idx += 1

        # Eyebrows (17-26)
        for i in range(10):
            ratio = i / 9.0
            lx = x + fw * (0.2 + ratio * 0.6)
            ly = y + fh * 0.25
            landmarks[idx] = [lx, ly, 0]
            idx += 1

        # Nose bridge and tip (27-35)
        for i in range(9):
            lx = center_x
            ly = y + fh * (0.3 + i * 0.05)
            landmarks[idx] = [lx, ly, 0]
            idx += 1

        # Eyes (36-47) - use detected eyes if available
        if len(eyes) >= 2:
            for (ex, ey, ew, eh) in eyes[:2]:
                eye_center_x = x + ex + ew // 2
                eye_center_y = y + ey + eh // 2
                for j in range(6):
                    angle = j * np.pi / 3
                    lx = eye_center_x + ew * 0.3 * np.cos(angle)
                    ly = eye_center_y + eh * 0.3 * np.sin(angle)
                    landmarks[idx] = [lx, ly, 0]
                    idx += 1
        else:
            # Default eye positions
            for eye_x in [x + fw * 0.3, x + fw * 0.7]:
                eye_y = y + fh * 0.4
                for j in range(6):
                    angle = j * np.pi / 3
                    lx = eye_x + fw * 0.05 * np.cos(angle)
                    ly = eye_y + fh * 0.05 * np.sin(angle)
                    landmarks[idx] = [lx, ly, 0]
                    idx += 1

        # Mouth (48-67)
        for i in range(20):
            ratio = i / 19.0
            lx = x + fw * (0.3 + ratio * 0.4)
            ly = y + fh * (0.7 + 0.05 * np.sin(ratio * np.pi))
            landmarks[idx] = [lx, ly, 0]
            idx += 1

        # Fill remaining landmarks with distributed points across face
        while idx < 468:
            # Distribute remaining points across the face region
            grid_size = int(np.sqrt(468 - idx)) + 1
            for i in range(grid_size):
                for j in range(grid_size):
                    if idx >= 468:
                        break
                    lx = x + fw * (i / grid_size)
                    ly = y + fh * (j / grid_size)
                    landmarks[idx] = [lx, ly, 0]
                    idx += 1
                if idx >= 468:
                    break

        return landmarks

    def detect_and_draw(self, image: np.ndarray,
                       draw_tesselation: bool = True,
                       draw_contours: bool = True,
                       draw_irises: bool = True) -> Tuple[np.ndarray, Optional[List[np.ndarray]]]:
        """
        Detect facial landmarks and draw them on the image.

        Args:
            image: Input image in BGR format
            draw_tesselation: Whether to draw face mesh tesselation
            draw_contours: Whether to draw face contours
            draw_irises: Whether to draw iris landmarks

        Returns:
            Tuple of (annotated_image, landmarks)
        """
        h, w = image.shape[:2]
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

        # Create a copy for drawing
        annotated_image = image.copy()

        if len(faces) == 0:
            return annotated_image, None

        # Limit to max_num_faces
        faces = faces[:self.max_num_faces]

        # Extract and draw landmarks
        all_landmarks = []

        for (x, y, fw, fh) in faces:
            # Draw face rectangle
            if draw_contours:
                cv2.rectangle(annotated_image, (x, y), (x+fw, y+fh), (0, 255, 0), 2)

            # Generate landmarks
            landmarks = self._generate_landmarks(image, gray, x, y, fw, fh)
            all_landmarks.append(landmarks)

            # Draw some key landmarks
            if draw_tesselation:
                for i in range(0, len(landmarks), 10):  # Draw every 10th landmark
                    lx, ly = int(landmarks[i][0]), int(landmarks[i][1])
                    cv2.circle(annotated_image, (lx, ly), 1, (0, 255, 255), -1)

        return annotated_image, all_landmarks
    
    def close(self):
        """Release resources."""
        # No resources to release for OpenCV cascades
        pass

