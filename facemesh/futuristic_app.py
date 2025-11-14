"""
Advanced Futuristic Biometric Authentication Application
Complete system with enrollment, verification, and identification
"""

import cv2
import numpy as np
import time
from biometric_auth import BiometricAuthSystem
from futuristic_ui import FuturisticUI


class FuturisticBiometricApp:
    """
    Complete futuristic biometric authentication application.
    Supports enrollment, verification, and identification with advanced UI.
    """

    def __init__(self):
        self.auth_system = BiometricAuthSystem()
        self.ui = FuturisticUI()
        self.cap = None
        self.fps = 0
        self.frame_times = []

        # Application state
        self.mode = "IDENTIFY"  # IDENTIFY, ENROLL, VERIFY
        self.status = "SCANNING"
        self.authenticated_user = None
        self.confidence = 0.0

        # Enrollment state
        self.enrollment_name = None
        self.enrollment_frames = []
        self.enrollment_progress = 0.0

    def initialize_camera(self, camera_id: int = 0):
        """Initialize camera capture."""
        self.cap = cv2.VideoCapture(camera_id)
        if not self.cap.isOpened():
            raise RuntimeError("Failed to open camera")

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    def calculate_fps(self):
        """Calculate current FPS."""
        current_time = time.time()
        self.frame_times.append(current_time)
        self.frame_times = [t for t in self.frame_times if current_time - t < 1.0]
        self.fps = len(self.frame_times)

    def process_identify_mode(self, frame: np.ndarray, display: np.ndarray,
                             landmarks_list, face_region) -> np.ndarray:
        """Process identification mode."""
        if landmarks_list is not None:
            # Try to identify user
            identified, user_id, conf, _ = self.auth_system.identify(frame)

            if identified:
                self.status = "AUTHENTICATED"
                self.authenticated_user = user_id
                self.confidence = conf

                # Draw user info card
                user_info = {
                    "User ID": user_id,
                    "Status": "AUTHENTICATED",
                    "Confidence": f"{conf:.1%}",
                    "Access": "GRANTED"
                }
                display = self.ui.draw_info_card(display, user_info, position=(20, 300))
            else:
                self.status = "UNKNOWN"
                self.confidence = 0.0
                self.authenticated_user = None
        else:
            self.status = "NO FACE"
            self.confidence = 0.0

        return display

    def process_enroll_mode(self, frame: np.ndarray, display: np.ndarray,
                           landmarks_list, face_region) -> np.ndarray:
        """Process enrollment mode."""
        if landmarks_list is not None and self.enrollment_name:
            # Collect frames for enrollment
            required_frames = 5

            if len(self.enrollment_frames) < required_frames:
                # Add frame every 10 frames to get variety
                if len(self.enrollment_frames) == 0 or self.ui.animation_frame % 10 == 0:
                    self.enrollment_frames.append(frame.copy())
                    self.enrollment_progress = len(self.enrollment_frames) / required_frames
                    self.status = "CAPTURING"
            else:
                # Enroll user
                success, msg = self.auth_system.enroll_user(
                    self.enrollment_name,
                    self.enrollment_frames
                )

                if success:
                    self.status = "ENROLLED"
                    self.confidence = 1.0
                else:
                    self.status = "ENROLL FAILED"
                    self.confidence = 0.0

                # Reset enrollment
                self.enrollment_frames = []
                self.enrollment_name = None
                self.enrollment_progress = 0.0

            # Draw progress bar
            h, w = display.shape[:2]
            progress_pos = (w // 2 - 200, h - 100)
            display = self.ui.draw_progress_bar(
                display,
                self.enrollment_progress,
                progress_pos,
                width=400,
                label="ENROLLMENT"
            )
        else:
            self.status = "WAITING"


    def process_frame(self, frame: np.ndarray) -> np.ndarray:
        """Process frame with futuristic UI overlay."""
        start_time = time.time()
        self.calculate_fps()

        # Detect face
        landmarks_list = self.auth_system.detector.detect(frame)

        # Start with HUD frame
        title = f"BIOMETRIC SYSTEM - MODE: {self.mode}"
        display = self.ui.draw_hud_frame(frame, title)

        face_region = None
        if landmarks_list is not None and len(landmarks_list) > 0:
            # Get first face
            landmarks = landmarks_list[0]

            # Calculate face bounding box
            x_coords = landmarks[:, 0]
            y_coords = landmarks[:, 1]
            x, y = int(x_coords.min()), int(y_coords.min())
            w, h = int(x_coords.max() - x), int(y_coords.max() - y)
            face_region = (x, y, w, h)

            # Draw visual effects
            display = self.ui.draw_face_grid(display, face_region)
            display = self.ui.draw_scanning_effect(display, face_region)
            display = self.ui.draw_landmark_points(display, landmarks, style="futuristic")
            display = self.ui.draw_face_box_advanced(display, face_region,
                                                     self.status, self.confidence)

        # Process based on mode
        if self.mode == "IDENTIFY":
            display = self.process_identify_mode(frame, display, landmarks_list, face_region)
        elif self.mode == "ENROLL":
            display = self.process_enroll_mode(frame, display, landmarks_list, face_region)

        # Calculate processing time
        process_time = (time.time() - start_time) * 1000

        # Draw metrics panel
        db_stats = self.auth_system.database.get_statistics()
        metrics = {
            "FPS": self.fps,
            "Process": f"{process_time:.1f}ms",
            "Users": db_stats['total_users'],
            "Status": self.status
        }
        display = self.ui.draw_metrics_panel(display, metrics, position="right")

        # Update animations
        self.ui.update_animation()

        # Apply glow effect
        display = self.ui.apply_glow_effect(display, intensity=0.12)

        return display

    def run(self):
        """Run the application."""
        print("=" * 70)
        print("FUTURISTIC BIOMETRIC AUTHENTICATION SYSTEM")
        print("=" * 70)
        print("\nInitializing...")

        try:
            self.initialize_camera()
            print("✓ Camera initialized")
            print("\nControls:")
            print("  I - Identification mode")
            print("  E - Enrollment mode (then enter name)")
            print("  R - Reset status")
            print("  Q - Quit")
            print("\nStarting application...\n")

            while True:
                ret, frame = self.cap.read()
                if not ret:
                    break

                display = self.process_frame(frame)
                cv2.imshow('Futuristic Biometric Authentication', display)

                key = cv2.waitKey(1) & 0xFF

                if key == ord('q') or key == ord('Q'):
                    break
                elif key == ord('i') or key == ord('I'):
                    self.mode = "IDENTIFY"
                    self.status = "SCANNING"
                    print("Mode: IDENTIFY")
                elif key == ord('e') or key == ord('E'):
                    self.mode = "ENROLL"
                    self.status = "WAITING"
                    name = input("\nEnter name for enrollment: ")
                    if name:
                        self.enrollment_name = name
                        self.enrollment_frames = []
                        print(f"Enrolling: {name}")
                elif key == ord('r') or key == ord('R'):
                    self.status = "SCANNING"
                    self.authenticated_user = None
                    self.confidence = 0.0
                    print("Status reset")

        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.cleanup()

    def cleanup(self):
        """Clean up resources."""
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        self.auth_system.close()
        print("\n✓ Cleanup complete")


def main():
    """Main entry point."""
    app = FuturisticBiometricApp()
    app.run()


if __name__ == "__main__":
    main()
