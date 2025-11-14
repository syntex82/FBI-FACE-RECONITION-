"""
Biometric Authentication System Module
Implements enrollment and verification logic using face mesh biometrics.
"""

import numpy as np
from typing import Optional, Tuple, List
from face_mesh_detector import FaceMeshDetector
from biometric_features import BiometricFeatureExtractor
from biometric_database import BiometricDatabase


class BiometricAuthSystem:
    """
    Complete biometric authentication system.
    
    Provides:
    - User enrollment with multiple samples
    - 1:1 verification (verify claimed identity)
    - 1:N identification (identify from database)
    """
    
    def __init__(self, 
                 db_path: str = "biometric_db",
                 verification_threshold: float = 0.75,
                 identification_threshold: float = 0.70,
                 min_samples_for_enrollment: int = 3):
        """
        Initialize the authentication system.
        
        Args:
            db_path: Path to biometric database
            verification_threshold: Minimum similarity for verification (0-1)
            identification_threshold: Minimum similarity for identification (0-1)
            min_samples_for_enrollment: Minimum samples required for enrollment
        """
        self.detector = FaceMeshDetector(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        self.feature_extractor = BiometricFeatureExtractor(normalize=True)
        self.database = BiometricDatabase(db_path=db_path)
        
        self.verification_threshold = verification_threshold
        self.identification_threshold = identification_threshold
        self.min_samples_for_enrollment = min_samples_for_enrollment
        
    def extract_features_from_image(self, image: np.ndarray) -> Optional[np.ndarray]:
        """
        Extract biometric features from an image.
        
        Args:
            image: Input image in BGR format
            
        Returns:
            Feature vector or None if no face detected
        """
        # Detect face landmarks
        landmarks_list = self.detector.detect(image)
        
        if landmarks_list is None or len(landmarks_list) == 0:
            return None
        
        # Use first detected face
        landmarks = landmarks_list[0]
        
        # Extract features
        features = self.feature_extractor.extract_features(landmarks)
        
        return features
    
    def enroll_user(self, user_id: str, images: List[np.ndarray], 
                   metadata: Optional[dict] = None) -> Tuple[bool, str]:
        """
        Enroll a new user with multiple sample images.
        
        Args:
            user_id: Unique identifier for the user
            images: List of images for enrollment
            metadata: Optional user metadata (name, etc.)
            
        Returns:
            Tuple of (success, message)
        """
        if len(images) < self.min_samples_for_enrollment:
            return False, f"Need at least {self.min_samples_for_enrollment} samples for enrollment"
        
        # Extract features from all images
        feature_vectors = []
        for i, image in enumerate(images):
            features = self.extract_features_from_image(image)
            if features is None:
                return False, f"No face detected in image {i+1}"
            feature_vectors.append(features)
        
        # Check consistency of samples (they should be similar)
        if not self._check_sample_consistency(feature_vectors):
            return False, "Samples are not consistent. Please ensure all images are of the same person."
        
        # Enroll each feature vector
        for features in feature_vectors:
            self.database.enroll_user(user_id, features, metadata)
        
        return True, f"Successfully enrolled user '{user_id}' with {len(feature_vectors)} samples"
    
    def verify(self, user_id: str, image: np.ndarray) -> Tuple[bool, float, str]:
        """
        Verify if the image matches the claimed user identity (1:1 matching).
        
        Args:
            user_id: Claimed user identity
            image: Image to verify
            
        Returns:
            Tuple of (verified, confidence_score, message)
        """
        # Check if user exists
        templates = self.database.get_user_templates(user_id)
        if templates is None:
            return False, 0.0, f"User '{user_id}' not found in database"
        
        # Extract features from input image
        features = self.extract_features_from_image(image)
        if features is None:
            return False, 0.0, "No face detected in image"
        
        # Compare with all stored templates
        similarities = []
        for template in templates:
            similarity = self.feature_extractor.compute_similarity(features, template)
            similarities.append(similarity)
        
        # Use maximum similarity
        max_similarity = max(similarities)
        avg_similarity = np.mean(similarities)
        
        # Verification decision
        verified = max_similarity >= self.verification_threshold
        
        if verified:
            message = f"Verification successful (confidence: {max_similarity:.2%})"
        else:
            message = f"Verification failed (confidence: {max_similarity:.2%}, threshold: {self.verification_threshold:.2%})"
        
        return verified, max_similarity, message
    
    def identify(self, image: np.ndarray, top_k: int = 5) -> List[Tuple[str, float]]:
        """
        Identify the person in the image from the database (1:N matching).
        
        Args:
            image: Image to identify
            top_k: Number of top matches to return
            
        Returns:
            List of (user_id, confidence_score) tuples, sorted by confidence
        """
        # Extract features from input image
        features = self.extract_features_from_image(image)
        if features is None:
            return []
        
        # Compare with all users in database
        matches = []
        for user_id in self.database.get_all_users():
            templates = self.database.get_user_templates(user_id)
            
            # Compare with all templates for this user
            similarities = []
            for template in templates:
                similarity = self.feature_extractor.compute_similarity(features, template)
                similarities.append(similarity)
            
            # Use maximum similarity for this user
            max_similarity = max(similarities)
            matches.append((user_id, max_similarity))
        
        # Sort by similarity (descending)
        matches.sort(key=lambda x: x[1], reverse=True)
        
        # Filter by threshold and return top_k
        matches = [(user_id, score) for user_id, score in matches 
                  if score >= self.identification_threshold]
        
        return matches[:top_k]

    def _check_sample_consistency(self, feature_vectors: List[np.ndarray],
                                  min_similarity: float = 0.65) -> bool:
        """
        Check if enrollment samples are consistent (from same person).

        Args:
            feature_vectors: List of feature vectors
            min_similarity: Minimum required similarity between samples

        Returns:
            True if samples are consistent
        """
        if len(feature_vectors) < 2:
            return True

        # Compare all pairs
        for i in range(len(feature_vectors)):
            for j in range(i + 1, len(feature_vectors)):
                similarity = self.feature_extractor.compute_similarity(
                    feature_vectors[i],
                    feature_vectors[j]
                )
                if similarity < min_similarity:
                    return False

        return True

    def get_database_stats(self) -> dict:
        """Get statistics about the biometric database."""
        return self.database.get_database_stats()

    def delete_user(self, user_id: str) -> Tuple[bool, str]:
        """
        Delete a user from the database.

        Args:
            user_id: User identifier

        Returns:
            Tuple of (success, message)
        """
        success = self.database.delete_user(user_id)
        if success:
            return True, f"User '{user_id}' deleted successfully"
        else:
            return False, f"User '{user_id}' not found"

    def close(self):
        """Release resources."""
        self.detector.close()

