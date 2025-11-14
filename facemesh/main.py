"""
Face Mesh Biometric Authentication - Main Application
Real-time webcam-based biometric authentication system.
"""

import cv2
import numpy as np
import time
from biometric_auth import BiometricAuthSystem


class BiometricApp:
    """
    Main application for face mesh biometric authentication.
    
    Modes:
    - Enrollment: Capture multiple samples to enroll a new user
    - Verification: Verify a claimed identity
    - Identification: Identify a person from the database
    """
    
    def __init__(self):
        """Initialize the application."""
        self.auth_system = BiometricAuthSystem(
            db_path="biometric_db",
            verification_threshold=0.75,
            identification_threshold=0.70,
            min_samples_for_enrollment=3
        )
        self.cap = None
        
    def start_camera(self, camera_id: int = 0) -> bool:
        """
        Start the camera.
        
        Args:
            camera_id: Camera device ID (0 for default)
            
        Returns:
            True if camera started successfully
        """
        self.cap = cv2.VideoCapture(camera_id)
        if not self.cap.isOpened():
            print("Error: Could not open camera")
            return False
        
        # Set camera properties for better quality
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
        return True
    
    def stop_camera(self):
        """Stop the camera."""
        if self.cap is not None:
            self.cap.release()
        cv2.destroyAllWindows()
    
    def capture_frame(self) -> np.ndarray:
        """
        Capture a single frame from the camera.
        
        Returns:
            Captured frame
        """
        ret, frame = self.cap.read()
        if not ret:
            return None
        return frame
    
    def enroll_mode(self, user_id: str, num_samples: int = 5):
        """
        Enrollment mode: Capture multiple samples for a new user.
        
        Args:
            user_id: Unique identifier for the user
            num_samples: Number of samples to capture
        """
        print(f"\n=== ENROLLMENT MODE ===")
        print(f"Enrolling user: {user_id}")
        print(f"Samples to capture: {num_samples}")
        print("\nInstructions:")
        print("- Look directly at the camera")
        print("- Keep your face well-lit and centered")
        print("- Press SPACE to capture each sample")
        print("- Press ESC to cancel\n")
        
        if not self.start_camera():
            return
        
        captured_images = []
        
        while len(captured_images) < num_samples:
            frame = self.capture_frame()
            if frame is None:
                break
            
            # Display frame with instructions
            display_frame = frame.copy()
            text = f"Sample {len(captured_images) + 1}/{num_samples} - Press SPACE to capture"
            cv2.putText(display_frame, text, (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Draw face mesh
            annotated, landmarks = self.auth_system.detector.detect_and_draw(
                frame, draw_tesselation=True, draw_contours=True, draw_irises=True
            )
            
            if landmarks is not None:
                cv2.putText(annotated, "Face Detected!", (10, 60), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                display_frame = annotated
            else:
                cv2.putText(display_frame, "No Face Detected", (10, 60), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
            cv2.imshow('Enrollment', display_frame)
            
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord(' '):  # Space to capture
                if landmarks is not None:
                    captured_images.append(frame.copy())
                    print(f"Captured sample {len(captured_images)}/{num_samples}")
                    time.sleep(0.5)  # Brief pause
                else:
                    print("No face detected. Please try again.")
            elif key == 27:  # ESC to cancel
                print("Enrollment cancelled")
                self.stop_camera()
                return
        
        self.stop_camera()
        
        # Enroll the user
        print("\nProcessing enrollment...")
        metadata = {'name': user_id, 'enrollment_date': time.strftime('%Y-%m-%d %H:%M:%S')}
        success, message = self.auth_system.enroll_user(user_id, captured_images, metadata)
        
        print(f"\n{message}")
        
        if success:
            stats = self.auth_system.get_database_stats()
            print(f"Total users in database: {stats['total_users']}")
    
    def verify_mode(self, user_id: str):
        """
        Verification mode: Verify a claimed identity.
        
        Args:
            user_id: Claimed user identity
        """
        print(f"\n=== VERIFICATION MODE ===")
        print(f"Verifying identity: {user_id}")
        print("\nInstructions:")
        print("- Look directly at the camera")
        print("- Press SPACE to verify")
        print("- Press ESC to exit\n")
        
        if not self.start_camera():
            return
        
        while True:
            frame = self.capture_frame()
            if frame is None:
                break
            
            # Display frame
            display_frame = frame.copy()
            cv2.putText(display_frame, f"Verifying: {user_id}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
            cv2.putText(display_frame, "Press SPACE to verify", (10, 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

            # Draw face mesh
            annotated, landmarks = self.auth_system.detector.detect_and_draw(frame)
            if landmarks is not None:
                display_frame = annotated

            cv2.imshow('Verification', display_frame)

            key = cv2.waitKey(1) & 0xFF

            if key == ord(' '):  # Space to verify
                print("\nVerifying...")
                verified, confidence, message = self.auth_system.verify(user_id, frame)
                print(message)

                # Show result on screen
                result_frame = display_frame.copy()
                if verified:
                    color = (0, 255, 0)
                    text = f"VERIFIED! ({confidence:.2%})"
                else:
                    color = (0, 0, 255)
                    text = f"FAILED ({confidence:.2%})"

                cv2.putText(result_frame, text, (10, 100),
                           cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, 3)
                cv2.imshow('Verification', result_frame)
                cv2.waitKey(2000)  # Show result for 2 seconds

            elif key == 27:  # ESC to exit
                break

        self.stop_camera()

    def identify_mode(self):
        """
        Identification mode: Identify a person from the database.
        """
        print(f"\n=== IDENTIFICATION MODE ===")
        print("\nInstructions:")
        print("- Look directly at the camera")
        print("- Press SPACE to identify")
        print("- Press ESC to exit\n")

        if not self.start_camera():
            return

        while True:
            frame = self.capture_frame()
            if frame is None:
                break

            # Display frame
            display_frame = frame.copy()
            cv2.putText(display_frame, "Identification Mode", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
            cv2.putText(display_frame, "Press SPACE to identify", (10, 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)

            # Draw face mesh
            annotated, landmarks = self.auth_system.detector.detect_and_draw(frame)
            if landmarks is not None:
                display_frame = annotated

            cv2.imshow('Identification', display_frame)

            key = cv2.waitKey(1) & 0xFF

            if key == ord(' '):  # Space to identify
                print("\nIdentifying...")
                matches = self.auth_system.identify(frame, top_k=5)

                if matches:
                    print("\nTop matches:")
                    for i, (user_id, confidence) in enumerate(matches, 1):
                        print(f"{i}. {user_id}: {confidence:.2%}")

                    # Show top match on screen
                    result_frame = display_frame.copy()
                    top_user, top_confidence = matches[0]
                    text = f"Identified: {top_user} ({top_confidence:.2%})"
                    cv2.putText(result_frame, text, (10, 100),
                               cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 3)
                    cv2.imshow('Identification', result_frame)
                    cv2.waitKey(2000)  # Show result for 2 seconds
                else:
                    print("No match found in database")
                    result_frame = display_frame.copy()
                    cv2.putText(result_frame, "No Match Found", (10, 100),
                               cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)
                    cv2.imshow('Identification', result_frame)
                    cv2.waitKey(2000)

            elif key == 27:  # ESC to exit
                break

        self.stop_camera()

    def show_database_stats(self):
        """Display database statistics."""
        stats = self.auth_system.get_database_stats()
        print("\n=== DATABASE STATISTICS ===")
        print(f"Total users: {stats['total_users']}")
        print(f"Total templates: {stats['total_templates']}")
        print(f"Average templates per user: {stats['avg_templates_per_user']:.1f}")
        if stats['users']:
            print(f"\nEnrolled users:")
            for user in stats['users']:
                print(f"  - {user}")
        else:
            print("\nNo users enrolled yet.")

    def cleanup(self):
        """Cleanup resources."""
        self.stop_camera()
        self.auth_system.close()


def main():
    """Main entry point."""
    app = BiometricApp()

    while True:
        print("\n" + "="*50)
        print("FACE MESH BIOMETRIC AUTHENTICATION SYSTEM")
        print("="*50)
        print("\n1. Enroll new user")
        print("2. Verify user")
        print("3. Identify user")
        print("4. Show database statistics")
        print("5. Delete user")
        print("6. Exit")

        choice = input("\nEnter your choice (1-6): ").strip()

        if choice == '1':
            user_id = input("Enter user ID: ").strip()
            if user_id:
                num_samples = input("Number of samples (default 5): ").strip()
                num_samples = int(num_samples) if num_samples.isdigit() else 5
                app.enroll_mode(user_id, num_samples)
            else:
                print("Invalid user ID")

        elif choice == '2':
            user_id = input("Enter user ID to verify: ").strip()
            if user_id:
                app.verify_mode(user_id)
            else:
                print("Invalid user ID")

        elif choice == '3':
            app.identify_mode()

        elif choice == '4':
            app.show_database_stats()

        elif choice == '5':
            user_id = input("Enter user ID to delete: ").strip()
            if user_id:
                confirm = input(f"Are you sure you want to delete '{user_id}'? (yes/no): ").strip().lower()
                if confirm == 'yes':
                    success, message = app.auth_system.delete_user(user_id)
                    print(message)
            else:
                print("Invalid user ID")

        elif choice == '6':
            print("\nExiting...")
            app.cleanup()
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()

