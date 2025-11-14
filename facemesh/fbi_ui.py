"""
FBI-Style Visual Interface
Professional law enforcement aesthetic with split-screen, grid view, and advanced visualizations
"""

import cv2
import numpy as np
import math
from typing import List, Dict, Tuple, Optional


class FBIUI:
    """
    FBI-style visual interface for facial recognition system.
    Features split-screen display, grid view, confidence meters, and professional aesthetics.
    """

    def __init__(self):
        """Initialize FBI UI."""
        self.animation_frame = 0

        # FBI Color scheme (professional law enforcement)
        self.colors = {
            'fbi_blue': (139, 69, 19),      # Dark blue
            'fbi_gold': (0, 215, 255),      # Gold/yellow
            'white': (255, 255, 255),
            'black': (0, 0, 0),
            'red': (0, 0, 255),
            'green': (0, 255, 0),
            'yellow': (0, 255, 255),
            'gray': (128, 128, 128),
            'dark_gray': (50, 50, 50),
            'light_blue': (255, 200, 100),
            'orange': (0, 165, 255),
            'cyan': (255, 255, 0)
        }

    def update_animation(self):
        """Update animation frame counter."""
        self.animation_frame += 1
        if self.animation_frame > 1000:
            self.animation_frame = 0

    def draw_fbi_header(self, frame: np.ndarray, title: str = "FBI FACIAL RECOGNITION SYSTEM") -> np.ndarray:
        """
        Draw FBI-style header bar.

        Args:
            frame: Input frame
            title: Header title

        Returns:
            Frame with header
        """
        h, w = frame.shape[:2]

        # Draw header background
        cv2.rectangle(frame, (0, 0), (w, 60), self.colors['fbi_blue'], -1)

        # Draw gold accent line
        cv2.rectangle(frame, (0, 58), (w, 60), self.colors['fbi_gold'], -1)

        # Draw FBI seal placeholder (circle)
        cv2.circle(frame, (40, 30), 22, self.colors['fbi_gold'], 2)
        cv2.putText(frame, "FBI", (25, 37), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                   self.colors['fbi_gold'], 1, cv2.LINE_AA)

        # Draw title
        font_scale = 0.8
        thickness = 2
        text_size = cv2.getTextSize(title, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)[0]
        text_x = (w - text_size[0]) // 2

        cv2.putText(frame, title, (text_x, 38), cv2.FONT_HERSHEY_SIMPLEX,
                   font_scale, self.colors['white'], thickness, cv2.LINE_AA)

        return frame

    def draw_split_screen(self, left_frame: np.ndarray, right_frame: np.ndarray,
                         labels: Tuple[str, str] = ("LIVE FEED", "DATABASE MATCH")) -> np.ndarray:
        """
        Create split-screen display.

        Args:
            left_frame: Left side frame
            right_frame: Right side frame
            labels: Labels for left and right sides

        Returns:
            Combined split-screen frame
        """
        # Resize frames to same height
        target_height = 600
        left_resized = cv2.resize(left_frame, (int(left_frame.shape[1] * target_height / left_frame.shape[0]), target_height))
        right_resized = cv2.resize(right_frame, (int(right_frame.shape[1] * target_height / right_frame.shape[0]), target_height))

        # Create combined frame
        total_width = left_resized.shape[1] + right_resized.shape[1] + 20  # 20px gap
        combined = np.zeros((target_height + 100, total_width, 3), dtype=np.uint8)

        # Place frames
        combined[80:80+target_height, 0:left_resized.shape[1]] = left_resized
        combined[80:80+target_height, left_resized.shape[1]+20:] = right_resized

        # Draw labels
        cv2.putText(combined, labels[0], (10, 60), cv2.FONT_HERSHEY_SIMPLEX,
                   0.7, self.colors['fbi_gold'], 2, cv2.LINE_AA)
        cv2.putText(combined, labels[1], (left_resized.shape[1] + 30, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, self.colors['fbi_gold'], 2, cv2.LINE_AA)

        # Draw divider line
        divider_x = left_resized.shape[1] + 10
        cv2.line(combined, (divider_x, 70), (divider_x, target_height + 80),
                self.colors['fbi_gold'], 2)

        return combined

    def draw_match_grid(self, frame: np.ndarray, matches: List[Dict],
                       images: List[np.ndarray], position: Tuple[int, int] = (20, 100)) -> np.ndarray:
        """
        Draw grid of top matches.

        Args:
            frame: Input frame
            matches: List of match dictionaries
            images: List of match images
            position: Top-left position for grid

        Returns:
            Frame with match grid
        """
        x, y = position
        cell_width = 150
        cell_height = 180
        cols = 3

        for i, (match, img) in enumerate(zip(matches[:6], images[:6])):
            row = i // cols
            col = i % cols

            cell_x = x + col * (cell_width + 10)
            cell_y = y + row * (cell_height + 10)

            # Draw cell background
            cv2.rectangle(frame, (cell_x, cell_y),
                         (cell_x + cell_width, cell_y + cell_height),
                         self.colors['dark_gray'], -1)
            cv2.rectangle(frame, (cell_x, cell_y),
                         (cell_x + cell_width, cell_y + cell_height),
                         self.colors['fbi_gold'], 2)

    def draw_confidence_meter(self, frame: np.ndarray, confidence: float,
                             position: Tuple[int, int] = (20, 20),
                             label: str = "MATCH CONFIDENCE") -> np.ndarray:
        """
        Draw confidence meter with gauge visualization.

        Args:
            frame: Input frame
            confidence: Confidence value (0-1)
            position: Position for meter
            label: Label text

        Returns:
            Frame with confidence meter
        """
        x, y = position
        width = 300
        height = 120

        # Draw background panel
        cv2.rectangle(frame, (x, y), (x + width, y + height),
                     self.colors['dark_gray'], -1)
        cv2.rectangle(frame, (x, y), (x + width, y + height),
                     self.colors['fbi_gold'], 2)

        # Draw label
        cv2.putText(frame, label, (x + 10, y + 25), cv2.FONT_HERSHEY_SIMPLEX,
                   0.6, self.colors['white'], 1, cv2.LINE_AA)

        # Draw gauge background
        gauge_y = y + 45
        cv2.rectangle(frame, (x + 10, gauge_y), (x + width - 10, gauge_y + 30),
                     self.colors['black'], -1)

        # Draw gauge fill
        fill_width = int((width - 20) * confidence)

        # Color based on confidence
        if confidence >= 0.9:
            color = self.colors['green']
        elif confidence >= 0.75:
            color = self.colors['light_blue']
        elif confidence >= 0.5:
            color = self.colors['yellow']
        else:
            color = self.colors['red']

        cv2.rectangle(frame, (x + 10, gauge_y), (x + 10 + fill_width, gauge_y + 30),
                     color, -1)

        # Draw percentage
        percentage_text = f"{confidence:.1%}"
        text_size = cv2.getTextSize(percentage_text, cv2.FONT_HERSHEY_SIMPLEX, 1.2, 2)[0]
        text_x = x + (width - text_size[0]) // 2
        cv2.putText(frame, percentage_text, (text_x, gauge_y + 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, self.colors['white'], 2, cv2.LINE_AA)

        return frame

    def draw_match_info_panel(self, frame: np.ndarray, match_data: Dict,
                             position: Tuple[int, int] = (20, 20)) -> np.ndarray:
        """
        Draw detailed match information panel.

        Args:
            frame: Input frame
            match_data: Match information dictionary
            position: Panel position

        Returns:
            Frame with info panel
        """
        x, y = position
        width = 350
        height = 250

        # Draw panel background
        cv2.rectangle(frame, (x, y), (x + width, y + height),
                     self.colors['dark_gray'], -1)
        cv2.rectangle(frame, (x, y), (x + width, y + height),
                     self.colors['fbi_gold'], 3)

        # Draw header
        cv2.rectangle(frame, (x, y), (x + width, y + 35),
                     self.colors['fbi_blue'], -1)
        cv2.putText(frame, "MATCH DETAILS", (x + 10, y + 23),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, self.colors['fbi_gold'], 2, cv2.LINE_AA)

        # Draw information fields
        fields = [
            ("Person ID:", match_data.get('person_id', 'N/A')),
            ("Name:", match_data.get('name', 'Unknown')),
            ("Confidence:", f"{match_data.get('confidence', 0):.1%}"),
            ("Max Similarity:", f"{match_data.get('max_similarity', 0):.1%}"),
            ("Avg Similarity:", f"{match_data.get('avg_similarity', 0):.1%}"),
            ("Images in DB:", str(match_data.get('num_images', 0))),
            ("Match Status:", "POSITIVE" if match_data.get('is_match', False) else "NEGATIVE")
        ]

        line_y = y + 55
        for label, value in fields:
            # Draw label
            cv2.putText(frame, label, (x + 15, line_y),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.colors['fbi_gold'], 1, cv2.LINE_AA)

            # Draw value
            cv2.putText(frame, str(value), (x + 150, line_y),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.colors['white'], 1, cv2.LINE_AA)

            line_y += 25

        return frame

    def draw_status_indicator(self, frame: np.ndarray, status: str,
                             position: Tuple[int, int] = (20, 20)) -> np.ndarray:
        """
        Draw status indicator with pulsing animation.

        Args:
            frame: Input frame
            status: Status text (SCANNING, MATCH FOUND, NO MATCH, etc.)
            position: Indicator position

        Returns:
            Frame with status indicator
        """
        x, y = position

        # Determine color based on status
        if "MATCH" in status.upper() and "NO" not in status.upper():
            color = self.colors['green']
        elif "SCANNING" in status.upper():
            color = self.colors['yellow']
        elif "NO MATCH" in status.upper():
            color = self.colors['red']
        else:
            color = self.colors['gray']

        # Pulsing effect
        pulse = abs(math.sin(self.animation_frame * 0.1))
        alpha = 0.5 + 0.5 * pulse

        # Draw status box
        box_width = 250
        box_height = 50

        overlay = frame.copy()
        cv2.rectangle(overlay, (x, y), (x + box_width, y + box_height),
                     color, -1)
        cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

        cv2.rectangle(frame, (x, y), (x + box_width, y + box_height),
                     color, 3)

        # Draw status text
        text_size = cv2.getTextSize(status, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
        text_x = x + (box_width - text_size[0]) // 2
        text_y = y + (box_height + text_size[1]) // 2

        cv2.putText(frame, status, (text_x, text_y),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, self.colors['white'], 2, cv2.LINE_AA)

        return frame

    def draw_timeline(self, frame: np.ndarray, matches: List[Dict],
                     position: Tuple[int, int] = (20, 20),
                     width: int = 600) -> np.ndarray:
        """
        Draw timeline of recent matches.

        Args:
            frame: Input frame
            matches: List of recent matches
            position: Timeline position
            width: Timeline width

        Returns:
            Frame with timeline
        """
        x, y = position
        height = 100

        # Draw timeline background
        cv2.rectangle(frame, (x, y), (x + width, y + height),
                     self.colors['dark_gray'], -1)
        cv2.rectangle(frame, (x, y), (x + width, y + height),
                     self.colors['fbi_gold'], 2)

        # Draw title
        cv2.putText(frame, "RECENT MATCHES", (x + 10, y + 25),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, self.colors['white'], 1, cv2.LINE_AA)

        # Draw timeline line
        line_y = y + 60
        cv2.line(frame, (x + 20, line_y), (x + width - 20, line_y),
                self.colors['fbi_gold'], 2)

        # Draw match points
        if matches:
            num_points = min(len(matches), 10)
            spacing = (width - 40) // max(num_points - 1, 1)

            for i in range(num_points):
                point_x = x + 20 + i * spacing
                confidence = matches[i].get('confidence', 0)

                # Color based on confidence
                if confidence >= 0.75:
                    color = self.colors['green']
                elif confidence >= 0.5:
                    color = self.colors['yellow']
                else:
                    color = self.colors['red']

                cv2.circle(frame, (point_x, line_y), 6, color, -1)
                cv2.circle(frame, (point_x, line_y), 6, self.colors['white'], 1)

        return frame

