"""
FBI Dashboard - Complete profile display system
Shows comprehensive information about identified persons
"""

import cv2
import numpy as np
import json
import os
from typing import Dict, Optional
from fbi_system import FBIFacialRecognitionSystem
from fbi_ui import FBIUI

class FBIDashboard:
    def __init__(self, profiles_file: str = "fbi_profiles.json"):
        """Initialize FBI Dashboard."""
        self.system = FBIFacialRecognitionSystem()
        self.ui = FBIUI()
        self.profiles_file = profiles_file
        self.profiles = self._load_profiles()
        self.current_profile = None
        
    def _load_profiles(self) -> Dict:
        """Load profiles from JSON file."""
        if os.path.exists(self.profiles_file):
            with open(self.profiles_file, 'r') as f:
                return json.load(f)
        return {}
    
    def get_profile(self, person_id: str) -> Optional[Dict]:
        """Get profile for a person."""
        return self.profiles.get(person_id)
    
    def draw_dashboard(self, frame: np.ndarray, profile: Dict, match_data: Dict) -> np.ndarray:
        """
        Draw complete FBI dashboard with profile information.

        Args:
            frame: Camera frame
            profile: Person profile data
            match_data: Match information

        Returns:
            Frame with dashboard overlay
        """
        h, w = frame.shape[:2]

        # Create larger canvas for dashboard (1920x1080)
        dashboard_w = 1920
        dashboard_h = 1080
        dashboard = np.zeros((dashboard_h, dashboard_w, 3), dtype=np.uint8)

        # Draw FBI header
        dashboard = self.ui.draw_fbi_header(dashboard, "FBI IDENTIFICATION DASHBOARD")

        # Main content area with better spacing
        content_y = 120
        left_col_x = 80
        right_col_x = dashboard_w // 2 + 80
        line_spacing = 45
        
        # === LEFT COLUMN: PERSONAL INFORMATION ===
        self._draw_section_header(dashboard, "PERSONAL INFORMATION", left_col_x, content_y)
        content_y += 60

        info_items = [
            ("FULL NAME:", profile.get('full_name', 'N/A')),
            ("AGE:", str(profile.get('age', 'N/A'))),
            ("GENDER:", profile.get('gender', 'N/A')),
            ("DATE OF BIRTH:", profile.get('date_of_birth', 'N/A')),
            ("NATIONALITY:", profile.get('nationality', 'N/A')),
            ("", ""),
            ("HEIGHT:", profile.get('height', 'N/A')),
            ("WEIGHT:", profile.get('weight', 'N/A')),
            ("EYE COLOR:", profile.get('eye_color', 'N/A')),
            ("HAIR COLOR:", profile.get('hair_color', 'N/A')),
            ("BLOOD TYPE:", profile.get('blood_type', 'N/A')),
        ]

        for label, value in info_items:
            if label:
                self._draw_info_line(dashboard, label, value, left_col_x, content_y)
            content_y += line_spacing
        
        # === RIGHT COLUMN: PROFESSIONAL & STATUS ===
        content_y = 180
        self._draw_section_header(dashboard, "PROFESSIONAL INFORMATION", right_col_x, content_y)
        content_y += 60

        prof_items = [
            ("OCCUPATION:", profile.get('occupation', 'N/A')),
            ("CLEARANCE LEVEL:", profile.get('clearance_level', 'N/A')),
            ("", ""),
        ]

        for label, value in prof_items:
            if label:
                self._draw_info_line(dashboard, label, value, right_col_x, content_y)
            content_y += line_spacing

        # Criminal Record Section
        content_y += 30
        self._draw_section_header(dashboard, "CRIMINAL RECORD", right_col_x, content_y)
        content_y += 60
        
        criminal_record = profile.get('criminal_record', 'N/A')
        status = profile.get('status', 'UNKNOWN')
        risk_level = profile.get('risk_level', 'UNKNOWN')

        # Status color coding
        if status == "CLEAR":
            status_color = self.ui.colors['green']
        elif status == "WARNING":
            status_color = self.ui.colors['yellow']
        else:
            status_color = self.ui.colors['red']

        cv2.putText(dashboard, criminal_record, (right_col_x + 20, content_y),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.9, self.ui.colors['green'], 2)
        content_y += line_spacing

        cv2.putText(dashboard, f"STATUS: {status}", (right_col_x + 20, content_y),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.9, status_color, 2)
        content_y += line_spacing

        cv2.putText(dashboard, f"RISK LEVEL: {risk_level}", (right_col_x + 20, content_y),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.9, self.ui.colors['green'], 2)
        
        # === BOTTOM: MATCH INFORMATION ===
        bottom_y = dashboard_h - 350
        self._draw_section_header(dashboard, "MATCH INFORMATION", left_col_x, bottom_y)
        bottom_y += 60

        confidence = match_data.get('confidence', 0) * 100
        match_status = "POSITIVE MATCH" if match_data.get('is_match') else "NO MATCH"
        match_color = self.ui.colors['green'] if match_data.get('is_match') else self.ui.colors['red']

        cv2.putText(dashboard, f"CONFIDENCE: {confidence:.1f}%", (left_col_x + 20, bottom_y),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, self.ui.colors['fbi_gold'], 3)
        bottom_y += 60

        cv2.putText(dashboard, f"STATUS: {match_status}", (left_col_x + 20, bottom_y),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, match_color, 3)

        # Draw confidence meter
        self.ui.draw_confidence_meter(dashboard, match_data.get('confidence', 0),
                                     (right_col_x, dashboard_h - 320), "MATCH CONFIDENCE")

        # Notes section
        notes_y = dashboard_h - 150
        notes = profile.get('notes', '')
        if notes:
            cv2.putText(dashboard, "NOTES:", (left_col_x, notes_y),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, self.ui.colors['fbi_gold'], 2)
            cv2.putText(dashboard, notes, (left_col_x + 150, notes_y),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, self.ui.colors['white'], 2)

        # Instructions
        cv2.putText(dashboard, "Press D to toggle | Q to Quit | F for Fullscreen | R for Report",
                   (left_col_x, dashboard_h - 50),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, self.ui.colors['yellow'], 2)

        return dashboard
    
    def _draw_section_header(self, frame: np.ndarray, title: str, x: int, y: int):
        """Draw section header."""
        cv2.putText(frame, title, (x, y),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.0, self.ui.colors['fbi_gold'], 3)
        cv2.line(frame, (x, y + 10), (x + 600, y + 10), self.ui.colors['fbi_gold'], 3)

    def _draw_info_line(self, frame: np.ndarray, label: str, value: str, x: int, y: int):
        """Draw information line."""
        cv2.putText(frame, label, (x + 20, y),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, self.ui.colors['fbi_gold'], 2)
        cv2.putText(frame, str(value), (x + 350, y),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, self.ui.colors['white'], 2)

