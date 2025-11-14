"""
Quick enrollment script for Michael
Deletes existing and re-enrolls with images
"""

import glob
import os
from fbi_system import FBIFacialRecognitionSystem

print("=" * 70)
print("QUICK ENROLLMENT - MICHAEL")
print("=" * 70)
print()

system = FBIFacialRecognitionSystem()

# Delete if exists
print("Checking for existing person...")
if system.database.get_person("michael"):
    print("Found existing 'michael' - deleting...")
    success, msg = system.database.delete_person("michael")
    print(f"  {msg}")

# Find images
image_folder = "enrollment_images/michael"
if not os.path.exists(image_folder):
    print(f"Error: Folder not found: {image_folder}")
    system.close()
    exit(1)

image_paths = []
for ext in ['*.jpg', '*.jpeg', '*.png']:
    image_paths.extend(glob.glob(os.path.join(image_folder, ext)))

if not image_paths:
    print(f"Error: No images found in {image_folder}")
    system.close()
    exit(1)

print(f"\nFound {len(image_paths)} images")
print("Enrolling Michael Blenkinsop...")

# Enroll
success, message = system.enroll_person_from_images(
    person_id="michael",
    name="Michael Blenkinsop",
    image_paths=image_paths,
    consent_obtained=True
)

if success:
    print(f"\n✓ {message}")
    
    # Show stats
    stats = system.database.get_statistics()
    print(f"\nDatabase Statistics:")
    print(f"  Total Persons: {stats['total_persons']}")
    print(f"  Total Images: {stats['total_images']}")
    
    print("\n" + "=" * 70)
    print("ENROLLMENT COMPLETE!")
    print("=" * 70)
    print("\nNext step: Run the FBI app to test face matching")
    print("  python fbi_app.py")
else:
    print(f"\n✗ {message}")

system.close()

