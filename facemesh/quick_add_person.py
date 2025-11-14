"""
Quick Add Person to FBI Database
All-in-one tool: Capture photos → Enroll → Add profile
"""

import cv2
import os
import json
from datetime import datetime
from fbi_system import FBIFacialRecognitionSystem


def capture_photos(person_id):
    """Capture photos for enrollment."""
    print("\n" + "=" * 70)
    print("PHOTO CAPTURE")
    print("=" * 70)
    print("\nControls:")
    print("  SPACE - Capture photo")
    print("  Q - Finish and continue")
    print("\nTips:")
    print("  - Take 3-5 photos from different angles")
    print("  - Look straight, then turn head slightly left/right")
    print("  - Make sure lighting is good")
    print("  - No sunglasses or hats\n")
    
    # Create folder
    folder = os.path.join("enrollment_images", person_id)
    os.makedirs(folder, exist_ok=True)
    
    # Open camera
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print("Error: Cannot open camera")
        return []
    
    photo_count = 0
    photos = []
    
    print("Camera ready! Press SPACE to capture photos...\n")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Show frame
        display = frame.copy()
        cv2.putText(display, f"Photos captured: {photo_count}", (20, 40),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(display, "SPACE = Capture | Q = Done", (20, display.shape[0] - 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        
        cv2.imshow('Capture Photos', display)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord(' '):
            # Capture photo
            photo_count += 1
            filename = os.path.join(folder, f"photo_{photo_count}.jpg")
            cv2.imwrite(filename, frame)
            photos.append(filename)
            print(f"✓ Captured photo {photo_count}: {filename}")
            
        elif key == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
    print(f"\n✓ Captured {photo_count} photos")
    return photos


def enroll_person(person_id, name, photos):
    """Enroll person in database."""
    print("\n" + "=" * 70)
    print("ENROLLING IN DATABASE")
    print("=" * 70)
    
    system = FBIFacialRecognitionSystem()
    
    try:
        success, message = system.enroll_person_from_images(
            person_id, name, photos, consent_obtained=True
        )
        
        if success:
            print(f"\n✓ {message}")
            return True
        else:
            print(f"\n✗ Enrollment failed: {message}")
            return False
            
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return False
    finally:
        system.close()


def add_profile(person_id, profile_data):
    """Add profile to fbi_profiles.json."""
    print("\n" + "=" * 70)
    print("ADDING PROFILE INFORMATION")
    print("=" * 70)
    
    profiles_file = "fbi_profiles.json"
    
    # Load existing profiles
    if os.path.exists(profiles_file):
        with open(profiles_file, 'r') as f:
            profiles = json.load(f)
    else:
        profiles = {}
    
    # Add new profile
    profiles[person_id] = profile_data
    
    # Save
    with open(profiles_file, 'w') as f:
        json.dump(profiles, f, indent=2)
    
    print(f"✓ Profile added for {profile_data['full_name']}")


def main():
    """Main function."""
    print("=" * 70)
    print("QUICK ADD PERSON TO FBI DATABASE")
    print("=" * 70)
    print("\nThis tool will:")
    print("  1. Capture photos from your camera")
    print("  2. Enroll the person in the database")
    print("  3. Add their profile information")
    print()
    
    # Get person information
    print("STEP 1: PERSON INFORMATION")
    print("-" * 70)
    
    person_id = input("Enter Person ID (e.g., john_smith): ").strip().lower().replace(" ", "_")
    if not person_id:
        print("Error: Person ID required")
        return
    
    full_name = input("Enter Full Name (e.g., John Smith): ").strip()
    if not full_name:
        print("Error: Name required")
        return
    
    age = input("Enter Age: ").strip()
    gender = input("Enter Gender (Male/Female): ").strip()
    occupation = input("Enter Occupation: ").strip()
    nationality = input("Enter Nationality: ").strip()
    
    # Capture photos
    print("\nSTEP 2: CAPTURE PHOTOS")
    print("-" * 70)
    input("Press ENTER to start camera...")
    
    photos = capture_photos(person_id)
    
    if len(photos) < 1:
        print("\n✗ No photos captured. Aborting.")
        return
    
    # Enroll
    print("\nSTEP 3: ENROLL IN DATABASE")
    print("-" * 70)
    
    if not enroll_person(person_id, full_name, photos):
        print("\n✗ Enrollment failed. Aborting.")
        return
    
    # Add profile
    print("\nSTEP 4: ADD PROFILE")
    print("-" * 70)
    
    profile = {
        "person_id": person_id,
        "full_name": full_name,
        "age": int(age) if age.isdigit() else 0,
        "gender": gender,
        "occupation": occupation,
        "nationality": nationality,
        "criminal_record": "No Previous Convictions",
        "status": "CLEAR",
        "risk_level": "LOW",
        "clearance_level": "STANDARD",
        "notes": f"Added on {datetime.now().strftime('%Y-%m-%d')}"
    }
    
    add_profile(person_id, profile)
    
    # Done!
    print("\n" + "=" * 70)
    print("✓ SUCCESS!")
    print("=" * 70)
    print(f"\n{full_name} has been added to the FBI database!")
    print(f"  Person ID: {person_id}")
    print(f"  Photos: {len(photos)}")
    print(f"  Status: CLEAR")
    print("\nYou can now run the FBI app to test:")
    print("  python fbi_app_fixed.py")
    print()


if __name__ == "__main__":
    main()

