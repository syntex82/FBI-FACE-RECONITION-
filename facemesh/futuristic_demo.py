"""
Futuristic Face Mesh Biometric Authentication Demo
Advanced sci-fi themed visual interface with real-time biometric authentication
"""

import cv2
import numpy as np
import time
from biometric_auth import BiometricAuthSystem
from futuristic_ui import FuturisticUI


class FuturisticBiometricDemo:
    """
    Advanced biometric authentication demo with futuristic UI.
    """

    def __init__(self):
        self.auth_system = BiometricAuthSystem()
        self.ui = FuturisticUI()
        self.cap = None
        self.fps = 0
        self.frame_times = []
        self.current_mode = "SCANNING"
        self.authenticated_user = None
        self.confidence = 0.0

    def initialize_camera(self, camera_id: int = 0):
        """Initialize camera capture."""
        self.cap = cv2.VideoCapture(camera_id)
        if not self.cap.isOpened():
            raise RuntimeError("Failed to open camera")

        # Set camera properties for better quality
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.cap.set(cv2.CAP_PROP_FPS, 30)

    def calculate_fps(self):
        """Calculate current FPS."""
        current_time = time.time()
        self.frame_times.append(current_time)

        # Keep only last second of frame times
        self.frame_times = [t for t in self.frame_times if current_time - t < 1.0]

        self.fps = len(self.frame_times)

    def process_frame(self, frame: np.ndarray) -> np.ndarray:
        """Process frame with futuristic UI overlay."""
        start_time = time.time()

        # Calculate FPS
        self.calculate_fps()

        # Detect face
        landmarks_list = self.auth_system.detector.detect(frame)

        # Start with HUD frame
        display = self.ui.draw_hud_frame(frame, "BIOMETRIC AUTHENTICATION SYSTEM v2.0")

        if landmarks_list is not None and len(landmarks_list) > 0:
            # Get first face
            landmarks = landmarks_list[0]

            # Calculate face bounding box from landmarks
            x_coords = landmarks[:, 0]
            y_coords = landmarks[:, 1]
            x, y = int(x_coords.min()), int(y_coords.min())
            w, h = int(x_coords.max() - x), int(y_coords.max() - y)
            face_region = (x, y, w, h)

            # Draw face grid overlay
            display = self.ui.draw_face_grid(display, face_region)

            # Draw scanning effect
            display = self.ui.draw_scanning_effect(display, face_region)

            # Draw landmark points
            display = self.ui.draw_landmark_points(display, landmarks, style="futuristic")

            # Draw advanced face box
            display = self.ui.draw_face_box_advanced(display, face_region,
                                                     self.current_mode, self.confidence)

            # Try to identify user
            if self.current_mode == "SCANNING":
                identified, user_id, conf, _ = self.auth_system.identify(frame)
                if identified:
                    self.current_mode = "AUTHENTICATED"
                    self.authenticated_user = user_id
                    self.confidence = conf
                else:
                    self.confidence = 0.5  # Default scanning confidence
        else:
            # No face detected
            self.current_mode = "NO FACE"
            self.confidence = 0.0
            self.authenticated_user = None

        # Calculate processing time
        process_time = (time.time() - start_time) * 1000  # ms

        # Draw metrics panel
        metrics = {
            "FPS": self.fps,
            "Process Time": f"{process_time:.1f} ms",
            "Confidence": f"{self.confidence:.1%}",
            "Status": self.current_mode
        }
        display = self.ui.draw_metrics_panel(display, metrics, position="right")

        # Draw user info card if authenticated
        if self.authenticated_user:
            user_info = {
                "User ID": self.authenticated_user,
                "Status": "AUTHENTICATED",
                "Access Level": "GRANTED"
            }
            display = self.ui.draw_info_card(display, user_info, position=(20, 300))

        # Update animations
        self.ui.update_animation()

        # Apply subtle glow effect
        display = self.ui.apply_glow_effect(display, intensity=0.15)

        return display

    def run_demo(self):
        """Run the futuristic biometric demo."""
        print("=" * 60)
        print("FUTURISTIC BIOMETRIC AUTHENTICATION SYSTEM")
        print("=" * 60)
        print("\nInitializing camera...")

        try:
            self.initialize_camera()
            print("✓ Camera initialized")
            print("\nControls:")
            print("  SPACE - Reset authentication status")
            print("  Q     - Quit")
            print("\nStarting demo...\n")

            while True:
                ret, frame = self.cap.read()
                if not ret:
                    print("Failed to grab frame")
                    break

                # Process frame with futuristic UI
                display = self.process_frame(frame)

                # Show the result
                cv2.imshow('Futuristic Biometric Authentication', display)

                # Handle keyboard input
                key = cv2.waitKey(1) & 0xFF

                if key == ord('q') or key == ord('Q'):
                    print("\nShutting down...")
                    break
                elif key == ord(' '):
                    # Reset authentication
                    self.current_mode = "SCANNING"
                    self.authenticated_user = None
                    self.confidence = 0.0
                    print("Authentication reset")

        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.cleanup()

    def cleanup(self):
        """Clean up resources."""
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        self.auth_system.close()
        print("✓ Cleanup complete")


def main():
    """Main entry point."""
    demo = FuturisticBiometricDemo()
    demo.run_demo()


if __name__ == "__main__":
    main()
