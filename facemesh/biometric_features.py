"""
Biometric Feature Extractor Module
Extracts unique biometric features from facial landmarks for identification.
"""

import numpy as np
from typing import List, Tuple
from scipy.spatial import distance


class BiometricFeatureExtractor:
    """
    Extracts biometric features from facial landmarks.
    
    Features include:
    - Euclidean distances between key facial points
    - Facial ratios and proportions
    - Angular measurements
    - Geometric relationships
    """
    
    # Key landmark indices for feature extraction
    # Based on MediaPipe FaceMesh 468-point model
    LANDMARK_INDICES = {
        'left_eye_outer': 33,
        'left_eye_inner': 133,
        'right_eye_outer': 362,
        'right_eye_inner': 263,
        'left_eye_top': 159,
        'left_eye_bottom': 145,
        'right_eye_top': 386,
        'right_eye_bottom': 374,
        'nose_tip': 1,
        'nose_bridge': 6,
        'left_mouth': 61,
        'right_mouth': 291,
        'mouth_top': 13,
        'mouth_bottom': 14,
        'left_cheek': 234,
        'right_cheek': 454,
        'chin': 152,
        'forehead': 10,
        'left_eyebrow_inner': 70,
        'left_eyebrow_outer': 46,
        'right_eyebrow_inner': 300,
        'right_eyebrow_outer': 276,
    }
    
    def __init__(self, normalize: bool = True):
        """
        Initialize the feature extractor.
        
        Args:
            normalize: Whether to normalize features for scale invariance
        """
        self.normalize = normalize
        
    def extract_features(self, landmarks: np.ndarray) -> np.ndarray:
        """
        Extract biometric features from facial landmarks.
        
        Args:
            landmarks: Array of shape (468, 3) containing facial landmarks
            
        Returns:
            Feature vector as 1D numpy array
        """
        features = []
        
        # 1. Extract distance-based features
        distance_features = self._extract_distance_features(landmarks)
        features.extend(distance_features)
        
        # 2. Extract ratio-based features
        ratio_features = self._extract_ratio_features(landmarks)
        features.extend(ratio_features)
        
        # 3. Extract angular features
        angular_features = self._extract_angular_features(landmarks)
        features.extend(angular_features)
        
        # 4. Extract eye and mouth features
        eye_mouth_features = self._extract_eye_mouth_features(landmarks)
        features.extend(eye_mouth_features)
        
        # Convert to numpy array
        feature_vector = np.array(features)
        
        # Normalize if requested
        if self.normalize:
            feature_vector = self._normalize_features(feature_vector)
        
        return feature_vector
    
    def _extract_distance_features(self, landmarks: np.ndarray) -> List[float]:
        """Extract Euclidean distances between key facial points."""
        features = []
        idx = self.LANDMARK_INDICES
        
        # Inter-ocular distance (eye to eye)
        features.append(self._euclidean_distance(
            landmarks[idx['left_eye_inner']], 
            landmarks[idx['right_eye_inner']]
        ))
        
        # Eye to nose distances
        features.append(self._euclidean_distance(
            landmarks[idx['left_eye_inner']], 
            landmarks[idx['nose_tip']]
        ))
        features.append(self._euclidean_distance(
            landmarks[idx['right_eye_inner']], 
            landmarks[idx['nose_tip']]
        ))
        
        # Nose to mouth distance
        features.append(self._euclidean_distance(
            landmarks[idx['nose_tip']], 
            landmarks[idx['mouth_top']]
        ))
        
        # Mouth width
        features.append(self._euclidean_distance(
            landmarks[idx['left_mouth']], 
            landmarks[idx['right_mouth']]
        ))
        
        # Face height (forehead to chin)
        features.append(self._euclidean_distance(
            landmarks[idx['forehead']], 
            landmarks[idx['chin']]
        ))
        
        # Face width (cheek to cheek)
        features.append(self._euclidean_distance(
            landmarks[idx['left_cheek']], 
            landmarks[idx['right_cheek']]
        ))
        
        # Eyebrow distances
        features.append(self._euclidean_distance(
            landmarks[idx['left_eyebrow_inner']], 
            landmarks[idx['left_eyebrow_outer']]
        ))
        features.append(self._euclidean_distance(
            landmarks[idx['right_eyebrow_inner']], 
            landmarks[idx['right_eyebrow_outer']]
        ))
        
        return features

    def _extract_angular_features(self, landmarks: np.ndarray) -> List[float]:
        """Extract angular measurements from facial geometry."""
        features = []
        idx = self.LANDMARK_INDICES

        # Angle between eyes and nose
        angle1 = self._calculate_angle(
            landmarks[idx['left_eye_inner']],
            landmarks[idx['nose_tip']],
            landmarks[idx['right_eye_inner']]
        )
        features.append(angle1)

        # Angle of nose bridge
        angle2 = self._calculate_angle(
            landmarks[idx['forehead']],
            landmarks[idx['nose_bridge']],
            landmarks[idx['nose_tip']]
        )
        features.append(angle2)

        # Jaw angle (left side)
        angle3 = self._calculate_angle(
            landmarks[idx['left_cheek']],
            landmarks[idx['chin']],
            landmarks[idx['left_mouth']]
        )
        features.append(angle3)

        # Jaw angle (right side)
        angle4 = self._calculate_angle(
            landmarks[idx['right_cheek']],
            landmarks[idx['chin']],
            landmarks[idx['right_mouth']]
        )
        features.append(angle4)

        return features

    def _extract_eye_mouth_features(self, landmarks: np.ndarray) -> List[float]:
        """Extract detailed eye and mouth features."""
        features = []
        idx = self.LANDMARK_INDICES

        # Left eye aspect ratio
        left_eye_height = self._euclidean_distance(
            landmarks[idx['left_eye_top']],
            landmarks[idx['left_eye_bottom']]
        )
        features.append(left_eye_height)

        # Right eye aspect ratio
        right_eye_height = self._euclidean_distance(
            landmarks[idx['right_eye_top']],
            landmarks[idx['right_eye_bottom']]
        )
        features.append(right_eye_height)

        # Mouth height
        mouth_height = self._euclidean_distance(
            landmarks[idx['mouth_top']],
            landmarks[idx['mouth_bottom']]
        )
        features.append(mouth_height)

        # Symmetry features (left vs right)
        left_eye_nose = self._euclidean_distance(
            landmarks[idx['left_eye_inner']],
            landmarks[idx['nose_tip']]
        )
        right_eye_nose = self._euclidean_distance(
            landmarks[idx['right_eye_inner']],
            landmarks[idx['nose_tip']]
        )
        symmetry = abs(left_eye_nose - right_eye_nose)
        features.append(symmetry)

        return features

    def _euclidean_distance(self, point1: np.ndarray, point2: np.ndarray) -> float:
        """Calculate Euclidean distance between two 3D points."""
        return np.linalg.norm(point1 - point2)

    def _calculate_angle(self, point1: np.ndarray, point2: np.ndarray, point3: np.ndarray) -> float:
        """
        Calculate angle at point2 formed by point1-point2-point3.
        Returns angle in degrees.
        """
        vector1 = point1 - point2
        vector2 = point3 - point2

        # Calculate angle using dot product
        cos_angle = np.dot(vector1, vector2) / (
            np.linalg.norm(vector1) * np.linalg.norm(vector2) + 1e-6
        )
        # Clamp to valid range for arccos
        cos_angle = np.clip(cos_angle, -1.0, 1.0)
        angle = np.arccos(cos_angle)

        return np.degrees(angle)

    def _normalize_features(self, features: np.ndarray) -> np.ndarray:
        """
        Normalize features to have zero mean and unit variance.
        This makes the features scale-invariant.
        """
        mean = np.mean(features)
        std = np.std(features)

        if std < 1e-6:
            return features

        return (features - mean) / std

    def compute_similarity(self, features1: np.ndarray, features2: np.ndarray) -> float:
        """
        Compute similarity between two feature vectors.

        Args:
            features1: First feature vector
            features2: Second feature vector

        Returns:
            Similarity score between 0 and 1 (1 = identical)
        """
        # Use cosine similarity
        similarity = 1 - distance.cosine(features1, features2)
        return max(0.0, min(1.0, similarity))

    def compute_distance(self, features1: np.ndarray, features2: np.ndarray) -> float:
        """
        Compute distance between two feature vectors.

        Args:
            features1: First feature vector
            features2: Second feature vector

        Returns:
            Euclidean distance between feature vectors
        """
        return np.linalg.norm(features1 - features2)
    
    def _extract_ratio_features(self, landmarks: np.ndarray) -> List[float]:
        """Extract facial ratios and proportions."""
        features = []
        idx = self.LANDMARK_INDICES
        
        # Eye width to face width ratio
        eye_distance = self._euclidean_distance(
            landmarks[idx['left_eye_inner']], 
            landmarks[idx['right_eye_inner']]
        )
        face_width = self._euclidean_distance(
            landmarks[idx['left_cheek']], 
            landmarks[idx['right_cheek']]
        )
        features.append(eye_distance / (face_width + 1e-6))
        
        # Nose to face height ratio
        nose_mouth_dist = self._euclidean_distance(
            landmarks[idx['nose_tip']], 
            landmarks[idx['mouth_top']]
        )
        face_height = self._euclidean_distance(
            landmarks[idx['forehead']], 
            landmarks[idx['chin']]
        )
        features.append(nose_mouth_dist / (face_height + 1e-6))
        
        # Mouth width to face width ratio
        mouth_width = self._euclidean_distance(
            landmarks[idx['left_mouth']], 
            landmarks[idx['right_mouth']]
        )
        features.append(mouth_width / (face_width + 1e-6))
        
        # Eye height to width ratios
        left_eye_height = self._euclidean_distance(
            landmarks[idx['left_eye_top']], 
            landmarks[idx['left_eye_bottom']]
        )
        left_eye_width = self._euclidean_distance(
            landmarks[idx['left_eye_outer']], 
            landmarks[idx['left_eye_inner']]
        )
        features.append(left_eye_height / (left_eye_width + 1e-6))
        
        right_eye_height = self._euclidean_distance(
            landmarks[idx['right_eye_top']], 
            landmarks[idx['right_eye_bottom']]
        )
        right_eye_width = self._euclidean_distance(
            landmarks[idx['right_eye_outer']], 
            landmarks[idx['right_eye_inner']]
        )
        features.append(right_eye_height / (right_eye_width + 1e-6))
        
        return features

