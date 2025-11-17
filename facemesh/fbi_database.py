"""
FBI-Style Advanced Database Management System
Stores multiple images per person with metadata and consent tracking
"""

import os
import json
import pickle
import shutil
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import numpy as np


class FBIDatabase:
    """
    Advanced database for FBI-style facial recognition system.
    Stores multiple images per person with metadata, consent tracking, and search capabilities.
    """

    def __init__(self, db_path: str = "fbi_database"):
        """
        Initialize FBI database.

        Args:
            db_path: Path to database directory
        """
        self.db_path = db_path
        self.images_path = os.path.join(db_path, "images")
        self.metadata_file = os.path.join(db_path, "metadata.json")
        self.features_file = os.path.join(db_path, "features.pkl")

        # Create directories
        os.makedirs(self.images_path, exist_ok=True)

        # Load or initialize metadata
        self.metadata = self._load_metadata()

        # Load or initialize features
        self.features = self._load_features()

    def _load_metadata(self) -> Dict:
        """Load metadata from file."""
        if os.path.exists(self.metadata_file):
            with open(self.metadata_file, 'r') as f:
                return json.load(f)
        return {
            "persons": {},  # person_id -> person data
            "total_persons": 0,
            "total_images": 0,
            "created_date": datetime.now().isoformat(),
            "last_modified": datetime.now().isoformat()
        }

    def _save_metadata(self):
        """Save metadata to file."""
        self.metadata["last_modified"] = datetime.now().isoformat()
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, f, indent=2)

    def _load_features(self) -> Dict:
        """Load biometric features from file."""
        if os.path.exists(self.features_file):
            with open(self.features_file, 'rb') as f:
                return pickle.load(f)
        return {}  # person_id -> list of feature vectors

    def _save_features(self):
        """Save biometric features to file."""
        with open(self.features_file, 'wb') as f:
            pickle.dump(self.features, f)

    def add_person(self, person_id: str, name: str, metadata: Optional[Dict] = None) -> bool:
        """
        Add a new person to the database.

        Args:
            person_id: Unique identifier for the person
            name: Person's name
            metadata: Additional metadata (consent info, notes, etc.)

        Returns:
            True if successful, False if person already exists
        """
        if person_id in self.metadata["persons"]:
            return False

        self.metadata["persons"][person_id] = {
            "name": name,
            "person_id": person_id,
            "images": [],
            "date_added": datetime.now().isoformat(),
            "consent_obtained": metadata.get("consent_obtained", False) if metadata else False,
            "notes": metadata.get("notes", "") if metadata else "",
            "custom_metadata": metadata if metadata else {}
        }

        self.metadata["total_persons"] += 1
        self.features[person_id] = []

        self._save_metadata()
        self._save_features()

        return True

    def add_image(self, person_id: str, image_path: str, features: np.ndarray,
                  metadata: Optional[Dict] = None) -> Tuple[bool, str]:
        """
        Add an image for a person.

        Args:
            person_id: Person identifier
            image_path: Path to the image file
            features: Biometric feature vector
            metadata: Image metadata (source, quality, etc.)

        Returns:
            (success, message)
        """
        if person_id not in self.metadata["persons"]:
            return False, "Person not found in database"

        if not os.path.exists(image_path):
            return False, "Image file not found"

        # Generate unique image ID
        image_id = f"{person_id}_{len(self.metadata['persons'][person_id]['images'])}"

        # Copy image to database
        person_dir = os.path.join(self.images_path, person_id)
        os.makedirs(person_dir, exist_ok=True)

        ext = os.path.splitext(image_path)[1]
        dest_path = os.path.join(person_dir, f"{image_id}{ext}")
        shutil.copy2(image_path, dest_path)

        # Store image metadata
        image_data = {
            "image_id": image_id,
            "filename": os.path.basename(dest_path),
            "path": dest_path,
            "date_added": datetime.now().isoformat(),
            "source": metadata.get("source", "manual_upload") if metadata else "manual_upload",
            "quality_score": metadata.get("quality_score", 0.0) if metadata else 0.0,
            "custom_metadata": metadata if metadata else {}
        }

        self.metadata["persons"][person_id]["images"].append(image_data)
        self.metadata["total_images"] += 1

        # Store features
        if person_id not in self.features:
            self.features[person_id] = []
        self.features[person_id].append(features)

        # Save to disk
        self._save_metadata()
        self._save_features()

        return True, f"Image added successfully: {image_id}"


    def get_person(self, person_id: str) -> Optional[Dict]:
        """Get person data by ID."""
        return self.metadata["persons"].get(person_id)

    def get_all_persons(self) -> List[Dict]:
        """Get all persons in database."""
        return list(self.metadata["persons"].values())

    def search_persons(self, query: str) -> List[Dict]:
        """
        Search persons by name or ID.

        Args:
            query: Search query

        Returns:
            List of matching persons
        """
        query_lower = query.lower()
        results = []

        for person in self.metadata["persons"].values():
            if (query_lower in person["name"].lower() or
                query_lower in person["person_id"].lower()):
                results.append(person)

        return results

    def get_features(self, person_id: str) -> Optional[List[np.ndarray]]:
        """Get all feature vectors for a person."""
        return self.features.get(person_id)

    def get_all_features(self) -> Dict[str, List[np.ndarray]]:
        """Get all features in database."""
        return self.features

    def delete_person(self, person_id: str) -> Tuple[bool, str]:
        """
        Delete a person and all their images.

        Args:
            person_id: Person identifier

        Returns:
            (success, message)
        """
        if person_id not in self.metadata["persons"]:
            return False, "Person not found"

        # Delete images directory
        person_dir = os.path.join(self.images_path, person_id)
        if os.path.exists(person_dir):
            shutil.rmtree(person_dir)

        # Remove from metadata
        num_images = len(self.metadata["persons"][person_id]["images"])
        del self.metadata["persons"][person_id]
        self.metadata["total_persons"] -= 1
        self.metadata["total_images"] -= num_images

        # Remove features
        del self.features[person_id]

        self._save_metadata()
        self._save_features()

        return True, f"Person {person_id} deleted successfully"

    def get_statistics(self) -> Dict:
        """Get database statistics."""
        return {
            "total_persons": self.metadata["total_persons"],
            "total_images": self.metadata["total_images"],
            "created_date": self.metadata["created_date"],
            "last_modified": self.metadata["last_modified"],
            "avg_images_per_person": (
                self.metadata["total_images"] / self.metadata["total_persons"]
                if self.metadata["total_persons"] > 0 else 0
            )
        }

    def export_person_data(self, person_id: str) -> Optional[Dict]:
        """Export all data for a person."""
        if person_id not in self.metadata["persons"]:
            return None

        person_data = self.metadata["persons"][person_id].copy()
        person_data["num_features"] = len(self.features.get(person_id, []))

        return person_data

    def close(self):
        """Close database and save all data."""
        self._save_metadata()
        self._save_features()

