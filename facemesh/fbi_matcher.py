"""
FBI-Style Advanced Face Matching Engine
Sophisticated face comparison with multiple images per person and quality assessment
"""

import numpy as np
from typing import List, Dict, Tuple, Optional
from sklearn.metrics.pairwise import cosine_similarity
import cv2
from biometric_features import BiometricFeatureExtractor


class FBIMatcher:
    """
    Advanced face matching engine for FBI-style facial recognition.
    Handles multiple images per person with confidence scoring and quality assessment.
    """
    
    def __init__(self, threshold: float = 0.75):
        """
        Initialize FBI matcher.
        
        Args:
            threshold: Minimum similarity threshold for a match (0-1)
        """
        self.threshold = threshold
        self.feature_extractor = BiometricFeatureExtractor()
    
    def calculate_similarity(self, features1: np.ndarray, features2: np.ndarray) -> float:
        """
        Calculate similarity between two feature vectors.
        
        Args:
            features1: First feature vector
            features2: Second feature vector
        
        Returns:
            Similarity score (0-1)
        """
        # Reshape for sklearn
        f1 = features1.reshape(1, -1)
        f2 = features2.reshape(1, -1)
        
        # Calculate cosine similarity
        similarity = cosine_similarity(f1, f2)[0][0]
        
        # Convert to 0-1 range (cosine similarity is -1 to 1)
        similarity = (similarity + 1) / 2
        
        return float(similarity)
    
    def match_against_person(self, query_features: np.ndarray, 
                            person_features: List[np.ndarray]) -> Tuple[float, float, int]:
        """
        Match query features against all images of a person.
        
        Args:
            query_features: Query feature vector
            person_features: List of feature vectors for the person
        
        Returns:
            (max_similarity, avg_similarity, best_match_index)
        """
        if not person_features:
            return 0.0, 0.0, -1
        
        similarities = []
        for features in person_features:
            sim = self.calculate_similarity(query_features, features)
            similarities.append(sim)
        
        max_sim = max(similarities)
        avg_sim = np.mean(similarities)
        best_idx = similarities.index(max_sim)
        
        return max_sim, avg_sim, best_idx
    
    def match_against_database(self, query_features: np.ndarray, 
                               database_features: Dict[str, List[np.ndarray]],
                               top_k: int = 5) -> List[Dict]:
        """
        Match query features against entire database.
        
        Args:
            query_features: Query feature vector
            database_features: Dictionary of person_id -> list of feature vectors
            top_k: Number of top matches to return
        
        Returns:
            List of match results sorted by confidence
        """
        results = []
        
        for person_id, person_features in database_features.items():
            max_sim, avg_sim, best_idx = self.match_against_person(
                query_features, person_features
            )
            
            # Calculate confidence score (weighted combination)
            confidence = 0.7 * max_sim + 0.3 * avg_sim
            
            results.append({
                "person_id": person_id,
                "confidence": confidence,
                "max_similarity": max_sim,
                "avg_similarity": avg_sim,
                "best_match_index": best_idx,
                "num_images": len(person_features),
                "is_match": confidence >= self.threshold
            })
        
        # Sort by confidence (descending)
        results.sort(key=lambda x: x["confidence"], reverse=True)
        
        # Return top K
        return results[:top_k]
    
    def assess_image_quality(self, image: np.ndarray) -> Dict[str, float]:
        """
        Assess the quality of a face image.
        
        Args:
            image: Face image
        
        Returns:
            Dictionary with quality metrics
        """
        # Convert to grayscale if needed
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        
        # Calculate sharpness (Laplacian variance)
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        sharpness = laplacian.var()
        
        # Normalize sharpness to 0-1 (typical range 0-1000)
        sharpness_score = min(sharpness / 1000.0, 1.0)
        
        # Calculate brightness
        brightness = np.mean(gray) / 255.0
        
        # Brightness score (penalize too dark or too bright)
        if brightness < 0.3 or brightness > 0.8:
            brightness_score = 0.5
        else:
            brightness_score = 1.0 - abs(brightness - 0.55) / 0.25
        
        # Calculate contrast
        contrast = np.std(gray) / 128.0
        contrast_score = min(contrast, 1.0)
        
        # Overall quality score
        quality_score = (
            0.4 * sharpness_score +
            0.3 * brightness_score +
            0.3 * contrast_score
        )
        
        return {
            "quality_score": quality_score,
            "sharpness": sharpness_score,
            "brightness": brightness_score,
            "contrast": contrast_score
        }
    
    def extract_and_assess(self, image: np.ndarray, landmarks: np.ndarray) -> Tuple[np.ndarray, Dict]:
        """
        Extract features and assess quality in one step.
        
        Args:
            image: Face image
            landmarks: Facial landmarks
        
        Returns:
            (features, quality_metrics)
        """
        features = self.feature_extractor.extract_features(landmarks)
        quality = self.assess_image_quality(image)
        
        return features, quality

