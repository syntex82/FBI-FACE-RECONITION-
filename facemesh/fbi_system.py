"""
FBI-Style Facial Recognition System
Complete advanced system with database management, matching, logging, and professional UI
"""

import cv2
import numpy as np
import time
import os
from typing import List, Dict, Optional, Tuple
from datetime import datetime

from face_mesh_detector import FaceMeshDetector
from biometric_features import BiometricFeatureExtractor
from fbi_database import FBIDatabase
from fbi_matcher import FBIMatcher
from fbi_logger import FBILogger
from fbi_ui import FBIUI


class FBIFacialRecognitionSystem:
    """
    Complete FBI-style facial recognition system.
    Integrates all components for professional law enforcement grade facial recognition.
    """

    def __init__(self, db_path: str = "fbi_database", log_dir: str = "fbi_logs"):
        """
        Initialize FBI system.

        Args:
            db_path: Path to database directory
            log_dir: Path to log directory
        """
        print("Initializing FBI Facial Recognition System...")

        # Initialize components
        self.detector = FaceMeshDetector()
        self.feature_extractor = BiometricFeatureExtractor()
        self.database = FBIDatabase(db_path)
        self.matcher = FBIMatcher(threshold=0.75)
        self.logger = FBILogger(log_dir)
        self.ui = FBIUI()

        # Camera
        self.cap = None

        # State
        self.current_matches = []
        self.recent_matches = []
        self.fps = 0
        self.frame_times = []

        print("✓ System initialized successfully")

    def initialize_camera(self, camera_id: int = 0):
        """Initialize camera capture."""
        # Use DirectShow backend for Windows (more reliable)
        self.cap = cv2.VideoCapture(camera_id, cv2.CAP_DSHOW)
        if not self.cap.isOpened():
            raise RuntimeError("Failed to open camera")

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.cap.set(cv2.CAP_PROP_FPS, 30)

        print("✓ Camera initialized")

    def calculate_fps(self):
        """Calculate current FPS."""
        current_time = time.time()
        self.frame_times.append(current_time)
        self.frame_times = [t for t in self.frame_times if current_time - t < 1.0]
        self.fps = len(self.frame_times)

    def enroll_person_from_images(self, person_id: str, name: str,
                                  image_paths: List[str],
                                  consent_obtained: bool = True) -> Tuple[bool, str]:
        """
        Enroll a person from multiple images.

        Args:
            person_id: Unique person identifier
            name: Person's name
            image_paths: List of image file paths
            consent_obtained: Whether consent was obtained

        Returns:
            (success, message)
        """
        # Add person to database
        metadata = {
            "consent_obtained": consent_obtained,
            "notes": f"Enrolled on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        }

        if not self.database.add_person(person_id, name, metadata):
            return False, f"Person {person_id} already exists"

        # Process each image
        enrolled_count = 0
        for img_path in image_paths:
            if not os.path.exists(img_path):
                print(f"Warning: Image not found: {img_path}")
                continue

            # Load image
            image = cv2.imread(img_path)
            if image is None:
                print(f"Warning: Could not load image: {img_path}")
                continue

            # Detect face
            landmarks_list = self.detector.detect(image)
            if landmarks_list is None or len(landmarks_list) == 0:
                print(f"Warning: No face detected in: {img_path}")
                continue

            # Use first face
            landmarks = landmarks_list[0]

            # Extract features and assess quality
            features, quality = self.matcher.extract_and_assess(image, landmarks)

            # Add to database
            img_metadata = {
                "source": "manual_upload",
                "quality_score": quality['quality_score'],
                "sharpness": quality['sharpness'],
                "brightness": quality['brightness'],
                "contrast": quality['contrast']
            }

            success, msg = self.database.add_image(person_id, img_path, features, img_metadata)
            if success:
                enrolled_count += 1
            else:
                print(f"Warning: {msg}")

        # Log enrollment
        self.logger.log_event("enrollment", f"Enrolled {name} ({person_id})", {
            "person_id": person_id,
            "name": name,
            "images_enrolled": enrolled_count,
            "total_images_attempted": len(image_paths)
        })

        if enrolled_count == 0:
            self.database.delete_person(person_id)
            return False, "No faces detected in any images"

        return True, f"Successfully enrolled {name} with {enrolled_count} images"

    def identify_face(self, frame: np.ndarray) -> Tuple[Optional[Dict], Optional[np.ndarray]]:
        """
        Identify face in frame.

        Args:
            frame: Input frame

        Returns:
            (match_data, landmarks) or (None, None) if no face detected
        """
        # Detect face
        landmarks_list = self.detector.detect(frame)
        if landmarks_list is None or len(landmarks_list) == 0:
            return None, None

        # Use first face
        landmarks = landmarks_list[0]

        # Extract features
        features = self.feature_extractor.extract_features(landmarks)

        # Match against database
        all_features = self.database.get_all_features()
        matches = self.matcher.match_against_database(features, all_features, top_k=5)

        if not matches:
            return None, landmarks

        # Get best match
        best_match = matches[0]

        # Add person name to match data
        person_data = self.database.get_person(best_match['person_id'])
        if person_data:
            best_match['name'] = person_data['name']

        # Log match if confidence is high
        if best_match['is_match']:
            self.logger.log_match(best_match)
            self.recent_matches.append(best_match)
            if len(self.recent_matches) > 20:
                self.recent_matches.pop(0)

        self.current_matches = matches

        return best_match, landmarks


    def get_person_image(self, person_id: str, image_index: int = 0) -> Optional[np.ndarray]:
        """
        Get an image for a person from database.

        Args:
            person_id: Person identifier
            image_index: Index of image to retrieve

        Returns:
            Image or None if not found
        """
        person_data = self.database.get_person(person_id)
        if not person_data or not person_data['images']:
            return None

        if image_index >= len(person_data['images']):
            image_index = 0

        image_path = person_data['images'][image_index]['path']
        if os.path.exists(image_path):
            return cv2.imread(image_path)

        return None

    def get_database_stats(self) -> Dict:
        """Get database statistics."""
        return self.database.get_statistics()

    def get_match_logs(self, limit: int = 10) -> List[Dict]:
        """Get recent match logs."""
        return self.logger.get_recent_matches(limit)

    def export_report(self, output_file: str):
        """Export system report."""
        self.logger.generate_report(output_file)

    def close(self):
        """Close system and cleanup resources."""
        if self.cap:
            self.cap.release()
        self.database.close()
        cv2.destroyAllWindows()
        print("✓ System closed")

