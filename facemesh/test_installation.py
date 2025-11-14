"""
Test Installation Script
Verifies that all dependencies are installed correctly.
"""

import sys


def test_imports():
    """Test if all required packages can be imported."""
    print("Testing package imports...\n")
    
    packages = {
        'cv2': 'opencv-python',
        'numpy': 'numpy',
        'sklearn': 'scikit-learn',
        'scipy': 'scipy'
    }

    optional_packages = {
        'mediapipe': 'mediapipe (optional - using OpenCV instead)'
    }
    
    failed = []

    for package, pip_name in packages.items():
        try:
            __import__(package)
            print(f"✓ {pip_name} - OK")
        except ImportError as e:
            print(f"✗ {pip_name} - FAILED")
            failed.append(pip_name)

    # Check optional packages
    for package, pip_name in optional_packages.items():
        try:
            __import__(package)
            print(f"✓ {pip_name} - OK")
        except ImportError as e:
            print(f"ℹ {pip_name} - Not installed (using alternative)")

    if failed:
        print(f"\n❌ Installation incomplete. Missing packages: {', '.join(failed)}")
        print(f"\nInstall missing packages with:")
        print(f"pip install {' '.join(failed)}")
        return False
    else:
        print("\n✓ All required packages installed successfully!")
        return True


def test_modules():
    """Test if all custom modules can be imported."""
    print("\nTesting custom modules...\n")
    
    modules = [
        'face_mesh_detector',
        'biometric_features',
        'biometric_database',
        'biometric_auth'
    ]
    
    failed = []
    
    for module in modules:
        try:
            __import__(module)
            print(f"✓ {module}.py - OK")
        except ImportError as e:
            print(f"✗ {module}.py - FAILED: {e}")
            failed.append(module)
    
    if failed:
        print(f"\n❌ Some modules failed to import: {', '.join(failed)}")
        return False
    else:
        print("\n✓ All custom modules loaded successfully!")
        return True


def test_camera():
    """Test if camera is accessible."""
    print("\nTesting camera access...\n")
    
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("✗ Camera not accessible")
            print("  Make sure your webcam is connected and not in use by another application")
            return False
        
        ret, frame = cap.read()
        cap.release()
        
        if ret and frame is not None:
            print(f"✓ Camera accessible (Resolution: {frame.shape[1]}x{frame.shape[0]})")
            return True
        else:
            print("✗ Camera opened but failed to capture frame")
            return False
            
    except Exception as e:
        print(f"✗ Camera test failed: {e}")
        return False


def test_face_detection():
    """Test face mesh detection."""
    print("\nTesting face mesh detection...\n")
    
    try:
        from face_mesh_detector import FaceMeshDetector
        import numpy as np
        
        detector = FaceMeshDetector()
        
        # Create a dummy image
        dummy_image = np.zeros((480, 640, 3), dtype=np.uint8)
        
        # Try to detect (should return None for blank image)
        result = detector.detect(dummy_image)
        
        detector.close()
        
        print("✓ Face mesh detector initialized successfully")
        print("  (No face detected in test image - this is expected)")
        return True
        
    except Exception as e:
        print(f"✗ Face detection test failed: {e}")
        return False


def test_feature_extraction():
    """Test feature extraction."""
    print("\nTesting feature extraction...\n")
    
    try:
        from biometric_features import BiometricFeatureExtractor
        import numpy as np
        
        extractor = BiometricFeatureExtractor()
        
        # Create dummy landmarks (468 points with x, y, z coordinates)
        dummy_landmarks = np.random.rand(468, 3) * 100
        
        # Extract features
        features = extractor.extract_features(dummy_landmarks)
        
        print(f"✓ Feature extraction successful")
        print(f"  Feature vector size: {len(features)}")
        return True
        
    except Exception as e:
        print(f"✗ Feature extraction test failed: {e}")
        return False


def test_database():
    """Test database operations."""
    print("\nTesting database operations...\n")
    
    try:
        from biometric_database import BiometricDatabase
        import numpy as np
        import os
        import shutil
        
        # Use a test database
        test_db_path = "test_biometric_db"
        
        # Clean up if exists
        if os.path.exists(test_db_path):
            shutil.rmtree(test_db_path)
        
        db = BiometricDatabase(db_path=test_db_path)
        
        # Test enrollment
        test_features = np.random.rand(25)
        db.enroll_user("test_user", test_features, {"name": "Test User"})
        
        # Test retrieval
        templates = db.get_user_templates("test_user")
        
        # Clean up
        shutil.rmtree(test_db_path)
        
        if templates is not None and len(templates) == 1:
            print("✓ Database operations successful")
            return True
        else:
            print("✗ Database test failed: Could not retrieve enrolled user")
            return False
        
    except Exception as e:
        print(f"✗ Database test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("="*60)
    print("Face Mesh Biometric Authentication - Installation Test")
    print("="*60)
    
    tests = [
        ("Package Imports", test_imports),
        ("Custom Modules", test_modules),
        ("Camera Access", test_camera),
        ("Face Detection", test_face_detection),
        ("Feature Extraction", test_feature_extraction),
        ("Database Operations", test_database)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ {test_name} crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓ All tests passed! System is ready to use.")
        print("\nRun 'python main.py' to start the application.")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

