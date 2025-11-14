"""
Test FBI System - Verify all components work
"""

import os
import sys

print("=" * 70)
print("FBI SYSTEM - COMPONENT TEST")
print("=" * 70)
print()

# Test 1: Import all modules
print("Test 1: Importing FBI modules...")
try:
    from fbi_database import FBIDatabase
    from fbi_matcher import FBIMatcher
    from fbi_logger import FBILogger
    from fbi_ui import FBIUI
    from fbi_system import FBIFacialRecognitionSystem
    print("✓ All modules imported successfully")
except Exception as e:
    print(f"✗ Import failed: {e}")
    sys.exit(1)

# Test 2: Initialize components
print("\nTest 2: Initializing components...")
try:
    db = FBIDatabase("test_fbi_db")
    matcher = FBIMatcher()
    logger = FBILogger("test_fbi_logs")
    ui = FBIUI()
    print("✓ All components initialized")
except Exception as e:
    print(f"✗ Initialization failed: {e}")
    sys.exit(1)

# Test 3: Check database
print("\nTest 3: Checking database...")
try:
    stats = db.get_statistics()
    print(f"✓ Database accessible")
    print(f"  Total Persons: {stats['total_persons']}")
    print(f"  Total Images: {stats['total_images']}")
    
    if stats['total_persons'] > 0:
        print(f"\n  Enrolled persons:")
        persons = db.get_all_persons()
        for person in persons:
            print(f"    - {person['name']} ({person['person_id']}): {len(person['images'])} images")
    else:
        print("  ⚠ No persons enrolled yet")
        print("  Run: python capture_enrollment_images.py")
        print("  Then: python fbi_enroll.py")
except Exception as e:
    print(f"✗ Database check failed: {e}")

# Test 4: Check face detection
print("\nTest 4: Testing face detection...")
try:
    from face_mesh_detector import FaceMeshDetector
    import cv2
    import numpy as np
    
    detector = FaceMeshDetector()
    
    # Create a test image
    test_img = np.zeros((480, 640, 3), dtype=np.uint8)
    landmarks = detector.detect(test_img)
    
    print("✓ Face detector initialized")
    print(f"  Detected {len(landmarks) if landmarks else 0} faces in test image")
except Exception as e:
    print(f"✗ Face detection test failed: {e}")

# Test 5: Check camera availability
print("\nTest 5: Checking camera...")
try:
    import cv2
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            print("✓ Camera is accessible")
            print(f"  Resolution: {frame.shape[1]}x{frame.shape[0]}")
        else:
            print("⚠ Camera opened but can't read frames")
        cap.release()
    else:
        print("⚠ Camera not accessible")
        print("  Close other apps using camera and try again")
except Exception as e:
    print(f"✗ Camera check failed: {e}")

# Test 6: Check logs
print("\nTest 6: Checking logs...")
try:
    recent_matches = logger.get_recent_matches(5)
    print(f"✓ Logger accessible")
    print(f"  Recent matches: {len(recent_matches)}")
    
    if recent_matches:
        print(f"\n  Last match:")
        last = recent_matches[0]
        print(f"    Person: {last.get('person_id', 'N/A')}")
        print(f"    Confidence: {last.get('confidence', 0):.1%}")
        print(f"    Time: {last.get('timestamp', 'N/A')}")
except Exception as e:
    print(f"✗ Logger check failed: {e}")

# Cleanup test directories
print("\nCleaning up test directories...")
import shutil
if os.path.exists("test_fbi_db"):
    shutil.rmtree("test_fbi_db")
if os.path.exists("test_fbi_logs"):
    shutil.rmtree("test_fbi_logs")

print("\n" + "=" * 70)
print("SYSTEM TEST COMPLETE")
print("=" * 70)

# Check if ready to run
db_real = FBIDatabase("fbi_database")
stats_real = db_real.get_statistics()

if stats_real['total_persons'] > 0:
    print("\n✅ SYSTEM READY!")
    print(f"\nYou have {stats_real['total_persons']} person(s) enrolled.")
    print("\nRun the FBI app:")
    print("  python fbi_app.py")
else:
    print("\n⚠ SYSTEM NOT READY")
    print("\nNo persons enrolled yet. Follow these steps:")
    print("\n1. Capture images:")
    print("   python capture_enrollment_images.py")
    print("\n2. Enroll into database:")
    print("   python fbi_enroll.py")
    print("\n3. Run FBI app:")
    print("   python fbi_app.py")

db_real.close()

