"""
FBI-Style Match Logging and Reporting System
Tracks all matches, searches, and system events
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Optional
import csv


class FBILogger:
    """
    Advanced logging system for FBI-style facial recognition.
    Tracks matches, searches, and generates reports.
    """
    
    def __init__(self, log_dir: str = "fbi_logs"):
        """
        Initialize FBI logger.
        
        Args:
            log_dir: Directory for log files
        """
        self.log_dir = log_dir
        self.matches_file = os.path.join(log_dir, "matches.json")
        self.events_file = os.path.join(log_dir, "events.json")
        
        # Create log directory
        os.makedirs(log_dir, exist_ok=True)
        
        # Load existing logs
        self.matches = self._load_json(self.matches_file, [])
        self.events = self._load_json(self.events_file, [])
    
    def _load_json(self, filepath: str, default):
        """Load JSON file or return default."""
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return json.load(f)
        return default
    
    def _save_json(self, filepath: str, data):
        """Save data to JSON file."""
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def log_match(self, match_data: Dict):
        """
        Log a face match event.

        Args:
            match_data: Dictionary containing match information
        """
        # Convert numpy types to Python types for JSON serialization
        clean_data = {}
        for key, value in match_data.items():
            if hasattr(value, 'item'):  # numpy scalar
                clean_data[key] = value.item()
            elif isinstance(value, (bool, int, float, str)):
                clean_data[key] = value
            else:
                clean_data[key] = str(value)

        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "match",
            **clean_data
        }

        self.matches.append(log_entry)
        self._save_json(self.matches_file, self.matches)
    
    def log_event(self, event_type: str, description: str, metadata: Optional[Dict] = None):
        """
        Log a system event.
        
        Args:
            event_type: Type of event (search, enrollment, deletion, etc.)
            description: Event description
            metadata: Additional event data
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "description": description,
            "metadata": metadata or {}
        }
        
        self.events.append(log_entry)
        self._save_json(self.events_file, self.events)
    
    def get_recent_matches(self, limit: int = 10) -> List[Dict]:
        """Get most recent matches."""
        return self.matches[-limit:][::-1]  # Reverse for newest first
    
    def get_matches_by_person(self, person_id: str) -> List[Dict]:
        """Get all matches for a specific person."""
        return [m for m in self.matches if m.get("person_id") == person_id]
    
    def get_high_confidence_matches(self, threshold: float = 0.9) -> List[Dict]:
        """Get matches above confidence threshold."""
        return [m for m in self.matches if m.get("confidence", 0) >= threshold]
    
    def get_statistics(self) -> Dict:
        """Get logging statistics."""
        total_matches = len(self.matches)
        
        if total_matches == 0:
            return {
                "total_matches": 0,
                "total_events": len(self.events),
                "avg_confidence": 0.0,
                "high_confidence_matches": 0
            }
        
        confidences = [m.get("confidence", 0) for m in self.matches]
        
        return {
            "total_matches": total_matches,
            "total_events": len(self.events),
            "avg_confidence": sum(confidences) / len(confidences),
            "max_confidence": max(confidences),
            "min_confidence": min(confidences),
            "high_confidence_matches": len([c for c in confidences if c >= 0.9])
        }
    
    def export_matches_csv(self, output_file: str):
        """
        Export matches to CSV file.
        
        Args:
            output_file: Output CSV file path
        """
        if not self.matches:
            return
        
        # Get all unique keys
        keys = set()
        for match in self.matches:
            keys.update(match.keys())
        
        keys = sorted(keys)
        
        with open(output_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(self.matches)
    
    def generate_report(self, output_file: str):
        """
        Generate a detailed text report.
        
        Args:
            output_file: Output text file path
        """
        stats = self.get_statistics()
        recent_matches = self.get_recent_matches(20)
        
        with open(output_file, 'w') as f:
            f.write("=" * 70 + "\n")
            f.write("FBI-STYLE FACIAL RECOGNITION SYSTEM - REPORT\n")
            f.write("=" * 70 + "\n\n")
            
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("STATISTICS\n")
            f.write("-" * 70 + "\n")
            for key, value in stats.items():
                f.write(f"{key.replace('_', ' ').title()}: {value}\n")
            
            f.write("\n\nRECENT MATCHES (Last 20)\n")
            f.write("-" * 70 + "\n")
            
            for i, match in enumerate(recent_matches, 1):
                f.write(f"\n{i}. {match.get('timestamp', 'N/A')}\n")
                f.write(f"   Person ID: {match.get('person_id', 'Unknown')}\n")
                f.write(f"   Confidence: {match.get('confidence', 0):.2%}\n")
                f.write(f"   Max Similarity: {match.get('max_similarity', 0):.2%}\n")
    
    def clear_logs(self):
        """Clear all logs (use with caution)."""
        self.matches = []
        self.events = []
        self._save_json(self.matches_file, self.matches)
        self._save_json(self.events_file, self.events)

