"""
Biometric Database Manager Module
Handles storage and retrieval of biometric templates for authentication.
"""

import os
import pickle
import numpy as np
from typing import Dict, Optional, List, Tuple
from datetime import datetime


class BiometricDatabase:
    """
    Manages storage and retrieval of biometric templates.
    
    Each user has:
    - user_id: Unique identifier
    - templates: List of feature vectors (multiple samples for robustness)
    - metadata: Additional information (enrollment date, etc.)
    """
    
    def __init__(self, db_path: str = "biometric_db"):
        """
        Initialize the biometric database.
        
        Args:
            db_path: Directory path to store database files
        """
        self.db_path = db_path
        self.db_file = os.path.join(db_path, "biometric_data.pkl")
        self.database: Dict[str, Dict] = {}
        
        # Create database directory if it doesn't exist
        os.makedirs(db_path, exist_ok=True)
        
        # Load existing database
        self.load()
    
    def enroll_user(self, user_id: str, feature_vector: np.ndarray, 
                   metadata: Optional[Dict] = None) -> bool:
        """
        Enroll a new user or add a new template to existing user.
        
        Args:
            user_id: Unique identifier for the user
            feature_vector: Biometric feature vector
            metadata: Optional metadata (name, etc.)
            
        Returns:
            True if enrollment successful
        """
        if user_id not in self.database:
            # New user enrollment
            self.database[user_id] = {
                'templates': [feature_vector],
                'metadata': metadata or {},
                'enrollment_date': datetime.now().isoformat(),
                'last_updated': datetime.now().isoformat()
            }
        else:
            # Add template to existing user
            self.database[user_id]['templates'].append(feature_vector)
            self.database[user_id]['last_updated'] = datetime.now().isoformat()
        
        # Save to disk
        self.save()
        return True
    
    def get_user_templates(self, user_id: str) -> Optional[List[np.ndarray]]:
        """
        Retrieve all templates for a user.
        
        Args:
            user_id: User identifier
            
        Returns:
            List of feature vectors or None if user not found
        """
        if user_id in self.database:
            return self.database[user_id]['templates']
        return None
    
    def get_all_users(self) -> List[str]:
        """
        Get list of all enrolled user IDs.
        
        Returns:
            List of user IDs
        """
        return list(self.database.keys())
    
    def get_user_metadata(self, user_id: str) -> Optional[Dict]:
        """
        Get metadata for a user.
        
        Args:
            user_id: User identifier
            
        Returns:
            Metadata dictionary or None if user not found
        """
        if user_id in self.database:
            return self.database[user_id]['metadata']
        return None
    
    def delete_user(self, user_id: str) -> bool:
        """
        Delete a user from the database.
        
        Args:
            user_id: User identifier
            
        Returns:
            True if deletion successful, False if user not found
        """
        if user_id in self.database:
            del self.database[user_id]
            self.save()
            return True
        return False
    
    def update_user_metadata(self, user_id: str, metadata: Dict) -> bool:
        """
        Update metadata for a user.
        
        Args:
            user_id: User identifier
            metadata: New metadata dictionary
            
        Returns:
            True if update successful, False if user not found
        """
        if user_id in self.database:
            self.database[user_id]['metadata'].update(metadata)
            self.database[user_id]['last_updated'] = datetime.now().isoformat()
            self.save()
            return True
        return False
    
    def get_database_stats(self) -> Dict:
        """
        Get statistics about the database.
        
        Returns:
            Dictionary with database statistics
        """
        total_users = len(self.database)
        total_templates = sum(len(user_data['templates']) 
                            for user_data in self.database.values())
        
        return {
            'total_users': total_users,
            'total_templates': total_templates,
            'avg_templates_per_user': total_templates / total_users if total_users > 0 else 0,
            'users': list(self.database.keys())
        }
    
    def save(self) -> bool:
        """
        Save database to disk.
        
        Returns:
            True if save successful
        """
        try:
            with open(self.db_file, 'wb') as f:
                pickle.dump(self.database, f)
            return True
        except Exception as e:
            print(f"Error saving database: {e}")
            return False
    
    def load(self) -> bool:
        """
        Load database from disk.
        
        Returns:
            True if load successful
        """
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, 'rb') as f:
                    self.database = pickle.load(f)
                return True
            except Exception as e:
                print(f"Error loading database: {e}")
                self.database = {}
                return False
        return True

