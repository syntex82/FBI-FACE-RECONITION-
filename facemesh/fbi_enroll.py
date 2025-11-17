"""
FBI Database Enrollment Utility
Tool for enrolling persons into the FBI database
"""

import os
import glob
from fbi_system import FBIFacialRecognitionSystem


def enroll_from_folder():
    """Enroll a person from a folder of images."""
    print("=" * 70)
    print("FBI DATABASE ENROLLMENT UTILITY")
    print("=" * 70)
    print()
    
    system = FBIFacialRecognitionSystem()
    
    # Get person information
    person_id = input("Enter Person ID (unique identifier): ").strip()
    if not person_id:
        print("Error: Person ID cannot be empty")
        return
    
    name = input("Enter Person Name: ").strip()
    if not name:
        print("Error: Name cannot be empty")
        return
    
    # Get consent
    consent = input("Has consent been obtained? (yes/no): ").strip().lower()
    consent_obtained = consent in ['yes', 'y']
    
    # Get image folder
    folder_path = input("Enter path to folder containing images: ").strip()
    if not os.path.exists(folder_path):
        print(f"Error: Folder not found: {folder_path}")
        return
    
    # Find all image files
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp']
    image_paths = []
    
    for ext in image_extensions:
        image_paths.extend(glob.glob(os.path.join(folder_path, ext)))
        image_paths.extend(glob.glob(os.path.join(folder_path, ext.upper())))
    
    if not image_paths:
        print(f"Error: No images found in {folder_path}")
        return
    
    print(f"\nFound {len(image_paths)} images")
    print("Processing...")
    
    # Enroll person
    success, message = system.enroll_person_from_images(
        person_id, name, image_paths, consent_obtained
    )
    
    if success:
        print(f"\n✓ {message}")
        
        # Show statistics
        stats = system.get_database_stats()
        print(f"\nDatabase Statistics:")
        print(f"  Total Persons: {stats['total_persons']}")
        print(f"  Total Images: {stats['total_images']}")
        print(f"  Avg Images/Person: {stats['avg_images_per_person']:.1f}")
    else:
        print(f"\n✗ Enrollment failed: {message}")
    
    system.close()


def enroll_from_file_list():
    """Enroll a person from a list of image files."""
    print("=" * 70)
    print("FBI DATABASE ENROLLMENT UTILITY")
    print("=" * 70)
    print()
    
    system = FBIFacialRecognitionSystem()
    
    # Get person information
    person_id = input("Enter Person ID (unique identifier): ").strip()
    if not person_id:
        print("Error: Person ID cannot be empty")
        return
    
    name = input("Enter Person Name: ").strip()
    if not name:
        print("Error: Name cannot be empty")
        return
    
    # Get consent
    consent = input("Has consent been obtained? (yes/no): ").strip().lower()
    consent_obtained = consent in ['yes', 'y']
    
    # Get image paths
    print("\nEnter image paths (one per line, empty line to finish):")
    image_paths = []
    while True:
        path = input().strip()
        if not path:
            break
        if os.path.exists(path):
            image_paths.append(path)
        else:
            print(f"Warning: File not found: {path}")
    
    if not image_paths:
        print("Error: No valid image paths provided")
        return
    
    print(f"\nProcessing {len(image_paths)} images...")
    
    # Enroll person
    success, message = system.enroll_person_from_images(
        person_id, name, image_paths, consent_obtained
    )
    
    if success:
        print(f"\n✓ {message}")
        
        # Show statistics
        stats = system.get_database_stats()
        print(f"\nDatabase Statistics:")
        print(f"  Total Persons: {stats['total_persons']}")
        print(f"  Total Images: {stats['total_images']}")
        print(f"  Avg Images/Person: {stats['avg_images_per_person']:.1f}")
    else:
        print(f"\n✗ Enrollment failed: {message}")
    
    system.close()


def main():
    """Main entry point."""
    print("Select enrollment method:")
    print("1. Enroll from folder")
    print("2. Enroll from file list")
    print("3. Exit")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == '1':
        enroll_from_folder()
    elif choice == '2':
        enroll_from_file_list()
    elif choice == '3':
        print("Goodbye!")
    else:
        print("Invalid choice")


if __name__ == "__main__":
    main()

