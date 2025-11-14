"""
Example Usage of Face Mesh Biometric Authentication System
Demonstrates how to use the system programmatically.
"""

import cv2
import numpy as np
from biometric_auth import BiometricAuthSystem


def example_enrollment():
    """Example: Enroll a user with images from webcam."""
    print("=== Example: User Enrollment ===\n")
    
    # Initialize the authentication system
    auth_system = BiometricAuthSystem(
        db_path="biometric_db",
        verification_threshold=0.75,
        identification_threshold=0.70
    )
    
    # Capture images from webcam
    cap = cv2.VideoCapture(0)
    images = []
    
    print("Capturing 5 samples. Press SPACE to capture each sample...")
    
    while len(images) < 5:
        ret, frame = cap.read()
        if not ret:
            break
        
        cv2.imshow('Capture', frame)
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord(' '):
            images.append(frame.copy())
            print(f"Captured sample {len(images)}/5")
        elif key == 27:  # ESC
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
    # Enroll the user
    if len(images) >= 3:
        user_id = "john_doe"
        metadata = {'name': 'John Doe', 'department': 'Engineering'}
        success, message = auth_system.enroll_user(user_id, images, metadata)
        print(f"\n{message}")
    else:
        print("Not enough samples captured")
    
    auth_system.close()


def example_verification():
    """Example: Verify a user's identity."""
    print("\n=== Example: User Verification ===\n")
    
    # Initialize the authentication system
    auth_system = BiometricAuthSystem()
    
    # Capture a single image
    cap = cv2.VideoCapture(0)
    print("Press SPACE to capture image for verification...")
    
    image = None
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        cv2.imshow('Verification', frame)
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord(' '):
            image = frame.copy()
            break
        elif key == 27:  # ESC
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
    # Verify the user
    if image is not None:
        user_id = "john_doe"
        verified, confidence, message = auth_system.verify(user_id, image)
        print(f"\n{message}")
        print(f"Verified: {verified}")
        print(f"Confidence: {confidence:.2%}")
    
    auth_system.close()


def example_identification():
    """Example: Identify a user from the database."""
    print("\n=== Example: User Identification ===\n")
    
    # Initialize the authentication system
    auth_system = BiometricAuthSystem()
    
    # Capture a single image
    cap = cv2.VideoCapture(0)
    print("Press SPACE to capture image for identification...")
    
    image = None
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        cv2.imshow('Identification', frame)
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord(' '):
            image = frame.copy()
            break
        elif key == 27:  # ESC
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
    # Identify the user
    if image is not None:
        matches = auth_system.identify(image, top_k=5)
        
        if matches:
            print("\nTop matches:")
            for i, (user_id, confidence) in enumerate(matches, 1):
                print(f"{i}. User: {user_id}, Confidence: {confidence:.2%}")
        else:
            print("\nNo matches found in database")
    
    auth_system.close()


def example_batch_processing():
    """Example: Process multiple images from files."""
    print("\n=== Example: Batch Processing ===\n")
    
    auth_system = BiometricAuthSystem()
    
    # Example: Load images from files
    image_paths = [
        "sample1.jpg",
        "sample2.jpg",
        "sample3.jpg",
    ]
    
    images = []
    for path in image_paths:
        try:
            img = cv2.imread(path)
            if img is not None:
                images.append(img)
        except:
            print(f"Could not load {path}")
    
    if len(images) >= 3:
        # Enroll user with batch images
        success, message = auth_system.enroll_user("batch_user", images)
        print(message)
    
    auth_system.close()


def example_database_management():
    """Example: Manage the biometric database."""
    print("\n=== Example: Database Management ===\n")
    
    auth_system = BiometricAuthSystem()
    
    # Get database statistics
    stats = auth_system.get_database_stats()
    print(f"Total users: {stats['total_users']}")
    print(f"Total templates: {stats['total_templates']}")
    print(f"Users: {stats['users']}")
    
    # Delete a user
    # success, message = auth_system.delete_user("john_doe")
    # print(f"\n{message}")
    
    auth_system.close()


if __name__ == "__main__":
    print("Face Mesh Biometric Authentication - Example Usage")
    print("=" * 60)
    
    # Uncomment the example you want to run:
    # example_enrollment()
    # example_verification()
    # example_identification()
    # example_batch_processing()
    example_database_management()

