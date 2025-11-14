"""
Configuration File
Centralized configuration for the Face Mesh Biometric Authentication System.
"""

# Database Configuration
DATABASE_PATH = "biometric_db"

# Authentication Thresholds
# Higher values = more strict, lower false acceptance rate
# Lower values = more lenient, higher false acceptance rate
VERIFICATION_THRESHOLD = 0.75  # For 1:1 verification (0.0 to 1.0)
IDENTIFICATION_THRESHOLD = 0.70  # For 1:N identification (0.0 to 1.0)

# Enrollment Configuration
MIN_SAMPLES_FOR_ENROLLMENT = 3  # Minimum number of samples required
RECOMMENDED_SAMPLES = 5  # Recommended number of samples
SAMPLE_CONSISTENCY_THRESHOLD = 0.65  # Minimum similarity between enrollment samples

# Face Detection Configuration
MAX_NUM_FACES = 1  # Maximum number of faces to detect
REFINE_LANDMARKS = True  # Whether to refine landmarks around eyes and lips
MIN_DETECTION_CONFIDENCE = 0.5  # Minimum confidence for face detection (0.0 to 1.0)
MIN_TRACKING_CONFIDENCE = 0.5  # Minimum confidence for landmark tracking (0.0 to 1.0)
STATIC_IMAGE_MODE = False  # Set to True for processing static images

# Camera Configuration
DEFAULT_CAMERA_ID = 0  # Default camera device ID
CAMERA_WIDTH = 1280  # Camera frame width
CAMERA_HEIGHT = 720  # Camera frame height

# Feature Extraction Configuration
NORMALIZE_FEATURES = True  # Whether to normalize features for scale invariance

# Visualization Configuration
DRAW_TESSELATION = True  # Draw face mesh tesselation
DRAW_CONTOURS = True  # Draw face contours
DRAW_IRISES = True  # Draw iris landmarks

# UI Configuration
DISPLAY_WINDOW_NAME = "Face Mesh Biometric Authentication"
RESULT_DISPLAY_TIME = 2000  # Time to display results in milliseconds

# Performance Configuration
TARGET_FPS = 30  # Target frames per second for video processing

# Security Configuration
STORE_RAW_IMAGES = False  # Whether to store raw images (NOT RECOMMENDED)
ENABLE_LOGGING = True  # Enable logging of authentication attempts

# Advanced Configuration
# Landmark indices for key facial points (MediaPipe FaceMesh 468-point model)
LANDMARK_INDICES = {
    'left_eye_outer': 33,
    'left_eye_inner': 133,
    'right_eye_outer': 362,
    'right_eye_inner': 263,
    'left_eye_top': 159,
    'left_eye_bottom': 145,
    'right_eye_top': 386,
    'right_eye_bottom': 374,
    'nose_tip': 1,
    'nose_bridge': 6,
    'left_mouth': 61,
    'right_mouth': 291,
    'mouth_top': 13,
    'mouth_bottom': 14,
    'left_cheek': 234,
    'right_cheek': 454,
    'chin': 152,
    'forehead': 10,
    'left_eyebrow_inner': 70,
    'left_eyebrow_outer': 46,
    'right_eyebrow_inner': 300,
    'right_eyebrow_outer': 276,
}


def get_config():
    """
    Get configuration as a dictionary.
    
    Returns:
        Dictionary containing all configuration parameters
    """
    return {
        'database': {
            'path': DATABASE_PATH,
        },
        'authentication': {
            'verification_threshold': VERIFICATION_THRESHOLD,
            'identification_threshold': IDENTIFICATION_THRESHOLD,
        },
        'enrollment': {
            'min_samples': MIN_SAMPLES_FOR_ENROLLMENT,
            'recommended_samples': RECOMMENDED_SAMPLES,
            'consistency_threshold': SAMPLE_CONSISTENCY_THRESHOLD,
        },
        'detection': {
            'max_num_faces': MAX_NUM_FACES,
            'refine_landmarks': REFINE_LANDMARKS,
            'min_detection_confidence': MIN_DETECTION_CONFIDENCE,
            'min_tracking_confidence': MIN_TRACKING_CONFIDENCE,
            'static_image_mode': STATIC_IMAGE_MODE,
        },
        'camera': {
            'default_id': DEFAULT_CAMERA_ID,
            'width': CAMERA_WIDTH,
            'height': CAMERA_HEIGHT,
        },
        'features': {
            'normalize': NORMALIZE_FEATURES,
        },
        'visualization': {
            'draw_tesselation': DRAW_TESSELATION,
            'draw_contours': DRAW_CONTOURS,
            'draw_irises': DRAW_IRISES,
        },
        'ui': {
            'window_name': DISPLAY_WINDOW_NAME,
            'result_display_time': RESULT_DISPLAY_TIME,
        },
        'performance': {
            'target_fps': TARGET_FPS,
        },
        'security': {
            'store_raw_images': STORE_RAW_IMAGES,
            'enable_logging': ENABLE_LOGGING,
        },
    }


def print_config():
    """Print current configuration."""
    config = get_config()
    print("="*60)
    print("Current Configuration")
    print("="*60)
    for category, settings in config.items():
        print(f"\n{category.upper()}:")
        for key, value in settings.items():
            print(f"  {key}: {value}")


if __name__ == "__main__":
    print_config()

