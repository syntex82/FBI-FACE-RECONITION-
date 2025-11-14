"""
Test camera access for FBI system
"""

import cv2
import sys

print("=" * 70)
print("TESTING CAMERA ACCESS")
print("=" * 70)
print()

# Try different camera backends
backends = [
    (cv2.CAP_DSHOW, "DirectShow (Windows)"),
    (cv2.CAP_MSMF, "Media Foundation (Windows)"),
    (cv2.CAP_ANY, "Auto-detect"),
]

camera_found = False

for backend, name in backends:
    print(f"Trying {name}...")
    cap = cv2.VideoCapture(0, backend)
    
    if cap.isOpened():
        ret, frame = cap.read()
        if ret and frame is not None:
            print(f"✓ SUCCESS with {name}")
            print(f"  Resolution: {frame.shape[1]}x{frame.shape[0]}")
            print(f"  FPS: {cap.get(cv2.CAP_PROP_FPS)}")
            camera_found = True
            
            # Show a test frame
            cv2.imshow('Camera Test - Press Q to close', frame)
            print("\nCamera window opened. Press 'Q' to close.")
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                cv2.putText(frame, "Camera Working! Press Q to quit", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.imshow('Camera Test - Press Q to close', frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            cap.release()
            cv2.destroyAllWindows()
            break
        else:
            print(f"✗ Failed to read frame with {name}")
            cap.release()
    else:
        print(f"✗ Failed to open camera with {name}")

if not camera_found:
    print("\n" + "=" * 70)
    print("CAMERA ACCESS FAILED")
    print("=" * 70)
    print("\nPossible solutions:")
    print("1. Check Windows camera permissions:")
    print("   Settings → Privacy → Camera → Allow apps to access camera")
    print("2. Close other apps using the camera (Zoom, Teams, etc.)")
    print("3. Try a different camera if you have multiple")
    print("4. Restart your computer")
    print("\nSee CAMERA_TROUBLESHOOTING.md for more help")
    sys.exit(1)
else:
    print("\n" + "=" * 70)
    print("✓ CAMERA ACCESS SUCCESSFUL!")
    print("=" * 70)
    print("\nYour camera is working and ready for the FBI system!")

