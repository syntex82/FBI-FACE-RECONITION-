"""
Futuristic UI Components for Biometric Authentication System
Provides sci-fi themed visual effects, HUD overlays, and animations
"""

import cv2
import numpy as np
import time
import math
from typing import Tuple, List, Optional


class FuturisticUI:
    """
    Provides futuristic visual effects and HUD elements for the biometric system.
    """

    def __init__(self):
        self.scan_line_pos = 0
        self.scan_direction = 1
        self.animation_frame = 0
        self.pulse_value = 0
        self.particle_systems = []

        # Color schemes (BGR format)
        self.colors = {
            'cyan': (255, 255, 0),
            'neon_blue': (255, 100, 0),
            'neon_green': (0, 255, 100),
            'neon_pink': (255, 0, 255),
            'neon_orange': (0, 165, 255),
            'white': (255, 255, 255),
            'red': (0, 0, 255),
            'green': (0, 255, 0),
            'yellow': (0, 255, 255),
            'dark_bg': (20, 20, 20)
        }

    def draw_hud_frame(self, image: np.ndarray, title: str = "BIOMETRIC AUTHENTICATION SYSTEM") -> np.ndarray:
        """Draw main HUD frame with corners and title."""
        h, w = image.shape[:2]
        overlay = image.copy()

        # Corner brackets
        corner_len = 40
        thickness = 3
        color = self.colors['cyan']

        # Top-left
        cv2.line(overlay, (20, 20), (20 + corner_len, 20), color, thickness)
        cv2.line(overlay, (20, 20), (20, 20 + corner_len), color, thickness)

        # Top-right
        cv2.line(overlay, (w - 20, 20), (w - 20 - corner_len, 20), color, thickness)
        cv2.line(overlay, (w - 20, 20), (w - 20, 20 + corner_len), color, thickness)

        # Bottom-left
        cv2.line(overlay, (20, h - 20), (20 + corner_len, h - 20), color, thickness)
        cv2.line(overlay, (20, h - 20), (20, h - 20 - corner_len), color, thickness)

        # Bottom-right
        cv2.line(overlay, (w - 20, h - 20), (w - 20 - corner_len, h - 20), color, thickness)
        cv2.line(overlay, (w - 20, h - 20), (w - 20, h - 20 - corner_len), color, thickness)

        # Title bar
        title_bg_height = 50
        cv2.rectangle(overlay, (0, 0), (w, title_bg_height), (40, 40, 40), -1)
        cv2.rectangle(overlay, (0, title_bg_height), (w, title_bg_height + 2), color, -1)

        # Title text
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.8
        font_thickness = 2
        text_size = cv2.getTextSize(title, font, font_scale, font_thickness)[0]
        text_x = (w - text_size[0]) // 2
        text_y = (title_bg_height + text_size[1]) // 2

        # Glowing text effect
        cv2.putText(overlay, title, (text_x, text_y), font, font_scale, color, font_thickness + 2)
        cv2.putText(overlay, title, (text_x, text_y), font, font_scale, self.colors['white'], font_thickness)

        return overlay

    def draw_scanning_effect(self, image: np.ndarray, face_region: Optional[Tuple[int, int, int, int]] = None) -> np.ndarray:
        """Draw animated scanning lines over the image or face region."""
        overlay = image.copy()
        h, w = image.shape[:2]

        if face_region:
            x, y, fw, fh = face_region
        else:
            x, y, fw, fh = 0, 60, w, h - 60

        # Horizontal scanning line
        scan_y = y + int((self.scan_line_pos / 100.0) * fh)

        # Gradient effect for scan line
        for i in range(-3, 4):
            alpha = 1.0 - abs(i) / 3.0
            color = tuple(int(c * alpha) for c in self.colors['cyan'])
            if 0 <= scan_y + i < h:
                cv2.line(overlay, (x, scan_y + i), (x + fw, scan_y + i), color, 1)

        # Update scan position
        self.scan_line_pos += self.scan_direction * 2
        if self.scan_line_pos >= 100 or self.scan_line_pos <= 0:
            self.scan_direction *= -1

        return overlay



    def draw_face_grid(self, image: np.ndarray, face_region: Tuple[int, int, int, int]) -> np.ndarray:
        """Draw 3D-style grid overlay on detected face."""
        overlay = image.copy()
        x, y, fw, fh = face_region

        # Grid parameters
        grid_lines = 8
        color = self.colors['neon_green']

        # Vertical lines
        for i in range(grid_lines + 1):
            line_x = x + int((i / grid_lines) * fw)
            alpha = 0.3 if i % 2 == 0 else 0.15
            line_color = tuple(int(c * alpha) for c in color)
            cv2.line(overlay, (line_x, y), (line_x, y + fh), line_color, 1)

        # Horizontal lines with perspective effect
        for i in range(grid_lines + 1):
            line_y = y + int((i / grid_lines) * fh)
            alpha = 0.3 if i % 2 == 0 else 0.15
            line_color = tuple(int(c * alpha) for c in color)
            cv2.line(overlay, (x, line_y), (x + fw, line_y), line_color, 1)

        return overlay

    def draw_face_box_advanced(self, image: np.ndarray, face_region: Tuple[int, int, int, int],
                               status: str = "SCANNING", confidence: float = 0.0) -> np.ndarray:
        """Draw advanced bounding box with animated corners and status."""
        overlay = image.copy()
        x, y, fw, fh = face_region

        # Determine color based on status
        if status == "AUTHENTICATED":
            color = self.colors['neon_green']
        elif status == "DENIED":
            color = self.colors['red']
        elif status == "SCANNING":
            color = self.colors['cyan']
        else:
            color = self.colors['yellow']

        # Animated pulse effect
        pulse = abs(math.sin(self.animation_frame * 0.1))
        thickness = 2 + int(pulse * 2)

        # Corner brackets (animated)
        corner_len = 30 + int(pulse * 10)

        # Top-left
        cv2.line(overlay, (x, y), (x + corner_len, y), color, thickness)
        cv2.line(overlay, (x, y), (x, y + corner_len), color, thickness)

        # Top-right
        cv2.line(overlay, (x + fw, y), (x + fw - corner_len, y), color, thickness)
        cv2.line(overlay, (x + fw, y), (x + fw, y + corner_len), color, thickness)

        # Bottom-left
        cv2.line(overlay, (x, y + fh), (x + corner_len, y + fh), color, thickness)
        cv2.line(overlay, (x, y + fh), (x, y + fh - corner_len), color, thickness)

        # Bottom-right
        cv2.line(overlay, (x + fw, y + fh), (x + fw - corner_len, y + fh), color, thickness)
        cv2.line(overlay, (x + fw, y + fh), (x + fw, y + fh - corner_len), color, thickness)

        # Status label
        label_y = y - 10
        if label_y < 20:
            label_y = y + fh + 25

        # Status background
        status_text = f"{status} - {confidence:.1%}"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.6
        font_thickness = 2
        text_size = cv2.getTextSize(status_text, font, font_scale, font_thickness)[0]

        bg_x1 = x
        bg_y1 = label_y - text_size[1] - 5
        bg_x2 = x + text_size[0] + 10
        bg_y2 = label_y + 5

        cv2.rectangle(overlay, (bg_x1, bg_y1), (bg_x2, bg_y2), (0, 0, 0), -1)
        cv2.rectangle(overlay, (bg_x1, bg_y1), (bg_x2, bg_y2), color, 2)

        # Status text with glow
        cv2.putText(overlay, status_text, (x + 5, label_y), font, font_scale, color, font_thickness + 1)
        cv2.putText(overlay, status_text, (x + 5, label_y), font, font_scale, self.colors['white'], 1)

        return overlay

    def draw_landmark_points(self, image: np.ndarray, landmarks: np.ndarray,
                            style: str = "futuristic") -> np.ndarray:
        """Draw facial landmarks with futuristic styling."""
        overlay = image.copy()

        if style == "futuristic":
            # Draw every 10th landmark with glowing effect
            for i in range(0, len(landmarks), 10):
                x, y = int(landmarks[i][0]), int(landmarks[i][1])

                # Outer glow
                cv2.circle(overlay, (x, y), 4, self.colors['cyan'], -1)
                # Inner bright point
                cv2.circle(overlay, (x, y), 2, self.colors['white'], -1)

        elif style == "mesh":
            # Draw connections between nearby landmarks
            for i in range(0, len(landmarks) - 1, 15):
                x1, y1 = int(landmarks[i][0]), int(landmarks[i][1])
                x2, y2 = int(landmarks[i + 1][0]), int(landmarks[i + 1][1])

                cv2.line(overlay, (x1, y1), (x2, y2), self.colors['neon_blue'], 1)
                cv2.circle(overlay, (x1, y1), 2, self.colors['cyan'], -1)

        return overlay

    def draw_metrics_panel(self, image: np.ndarray, metrics: dict, position: str = "right") -> np.ndarray:
        """Draw real-time metrics panel with FPS, confidence, etc."""
        overlay = image.copy()
        h, w = image.shape[:2]

        # Panel dimensions
        panel_width = 280
        panel_height = 200
        margin = 20

        if position == "right":
            panel_x = w - panel_width - margin
        else:
            panel_x = margin

        panel_y = 70

        # Semi-transparent background
        panel_overlay = overlay.copy()
        cv2.rectangle(panel_overlay, (panel_x, panel_y),
                     (panel_x + panel_width, panel_y + panel_height),
                     (20, 20, 20), -1)
        cv2.addWeighted(panel_overlay, 0.7, overlay, 0.3, 0, overlay)

        # Border
        cv2.rectangle(overlay, (panel_x, panel_y),
                     (panel_x + panel_width, panel_y + panel_height),
                     self.colors['cyan'], 2)

        # Title
        cv2.putText(overlay, "SYSTEM METRICS", (panel_x + 10, panel_y + 25),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, self.colors['cyan'], 2)

        # Metrics
        y_offset = panel_y + 55
        line_height = 30

        for key, value in metrics.items():
            # Label
            cv2.putText(overlay, f"{key}:", (panel_x + 10, y_offset),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.colors['white'], 1)

            # Value
            value_str = f"{value:.2f}" if isinstance(value, float) else str(value)
            cv2.putText(overlay, value_str, (panel_x + 150, y_offset),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.colors['neon_green'], 2)

            y_offset += line_height

        return overlay

    def draw_progress_bar(self, image: np.ndarray, progress: float,
                         position: Tuple[int, int], width: int = 200,
                         label: str = "PROCESSING") -> np.ndarray:
        """Draw animated progress bar."""
        overlay = image.copy()
        x, y = position
        height = 25

        # Background
        cv2.rectangle(overlay, (x, y), (x + width, y + height), (40, 40, 40), -1)
        cv2.rectangle(overlay, (x, y), (x + width, y + height), self.colors['cyan'], 2)

        # Progress fill
        fill_width = int(width * progress)
        if fill_width > 0:
            # Gradient effect
            for i in range(fill_width):
                alpha = 0.5 + 0.5 * (i / fill_width)
                color = tuple(int(c * alpha) for c in self.colors['neon_green'])
                cv2.line(overlay, (x + i, y + 2), (x + i, y + height - 2), color, 1)

        # Label
        cv2.putText(overlay, f"{label}: {progress:.0%}", (x + 5, y - 5),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.colors['white'], 1)

        return overlay

    def draw_info_card(self, image: np.ndarray, user_info: dict,
                      position: Tuple[int, int] = (20, 300)) -> np.ndarray:
        """Draw user information card with futuristic styling."""
        overlay = image.copy()
        x, y = position

        card_width = 300
        card_height = 150

        # Card background
        card_overlay = overlay.copy()
        cv2.rectangle(card_overlay, (x, y), (x + card_width, y + card_height),
                     (30, 30, 30), -1)
        cv2.addWeighted(card_overlay, 0.8, overlay, 0.2, 0, overlay)

        # Border with glow
        cv2.rectangle(overlay, (x, y), (x + card_width, y + card_height),
                     self.colors['neon_blue'], 3)
        cv2.rectangle(overlay, (x - 2, y - 2), (x + card_width + 2, y + card_height + 2),
                     self.colors['neon_blue'], 1)

        # Title bar
        cv2.rectangle(overlay, (x, y), (x + card_width, y + 35),
                     self.colors['neon_blue'], -1)
        cv2.putText(overlay, "USER PROFILE", (x + 10, y + 23),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

        # User info
        y_offset = y + 60
        for key, value in user_info.items():
            text = f"{key}: {value}"
            cv2.putText(overlay, text, (x + 15, y_offset),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.colors['white'], 1)
            y_offset += 25

        return overlay

    def update_animation(self):
        """Update animation frame counter."""
        self.animation_frame += 1
        if self.animation_frame > 1000:
            self.animation_frame = 0

    def apply_glow_effect(self, image: np.ndarray, intensity: float = 0.3) -> np.ndarray:
        """Apply subtle glow effect to the entire image."""
        blurred = cv2.GaussianBlur(image, (15, 15), 0)
        return cv2.addWeighted(image, 1.0, blurred, intensity, 0)

