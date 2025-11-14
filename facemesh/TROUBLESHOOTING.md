# Troubleshooting Guide

Common issues and solutions for the Face Mesh Biometric Authentication System.

## Installation Issues

### Issue: "ModuleNotFoundError: No module named 'cv2'"
**Solution**:
```bash
pip install opencv-python
```

### Issue: "ModuleNotFoundError: No module named 'mediapipe'"
**Solution**:
```bash
pip install mediapipe
```

### Issue: All packages fail to install
**Solution**:
```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Install all dependencies
pip install -r requirements.txt
```

## Camera Issues

### Issue: "Error: Could not open camera"
**Possible Solutions**:

1. **Check if camera is in use**:
   - Close other applications using the camera (Zoom, Skype, etc.)
   - Restart your computer

2. **Try different camera ID**:
   ```python
   # In main.py or your code, try:
   app.start_camera(camera_id=1)  # or 2, 3, etc.
   ```

3. **Check camera permissions**:
   - Windows: Settings → Privacy → Camera
   - macOS: System Preferences → Security & Privacy → Camera
   - Linux: Check device permissions for `/dev/video0`

4. **Test camera separately**:
   ```python
   import cv2
   cap = cv2.VideoCapture(0)
   print(cap.isOpened())  # Should print True
   ```

### Issue: Camera opens but shows black screen
**Solution**:
- Wait a few seconds for camera to initialize
- Check camera lens is not covered
- Try unplugging and replugging USB camera
- Update camera drivers

## Face Detection Issues

### Issue: "No face detected"
**Possible Solutions**:

1. **Improve lighting**:
   - Face the light source
   - Avoid backlighting
   - Use natural or bright artificial light

2. **Adjust position**:
   - Move closer to camera (2-3 feet optimal)
   - Center your face in the frame
   - Look directly at camera

3. **Remove obstructions**:
   - Remove hands from face
   - Ensure hair doesn't cover face
   - Remove large glasses if possible

4. **Lower detection threshold**:
   ```python
   # In config.py or when creating detector
   MIN_DETECTION_CONFIDENCE = 0.3  # Lower from 0.5
   ```

### Issue: Face detection is slow/laggy
**Solution**:
1. Close other applications
2. Reduce camera resolution in config.py:
   ```python
   CAMERA_WIDTH = 640
   CAMERA_HEIGHT = 480
   ```
3. Disable some visualization:
   ```python
   DRAW_TESSELATION = False
   ```

## Authentication Issues

### Issue: "Verification failed" with low confidence
**Possible Solutions**:

1. **Re-enroll with more samples**:
   - Use 7-10 samples instead of 5
   - Ensure consistent lighting during enrollment

2. **Check enrollment quality**:
   - All enrollment samples should be clear
   - Face should be well-lit in all samples
   - Maintain similar distance in all samples

3. **Adjust threshold**:
   ```python
   # In config.py
   VERIFICATION_THRESHOLD = 0.65  # Lower from 0.75
   ```

4. **Use consistent conditions**:
   - Same lighting as enrollment
   - Same glasses/no glasses as enrollment
   - Similar facial expression

### Issue: "Samples are not consistent" during enrollment
**Solution**:
1. Ensure all samples are of the same person
2. Use better lighting
3. Keep face at consistent distance
4. Lower consistency threshold:
   ```python
   # In config.py
   SAMPLE_CONSISTENCY_THRESHOLD = 0.55  # Lower from 0.65
   ```

### Issue: False positives (wrong person verified)
**Solution**:
1. Increase verification threshold:
   ```python
   VERIFICATION_THRESHOLD = 0.85  # Increase from 0.75
   ```
2. Enroll with more samples (7-10)
3. Ensure enrollment samples are high quality

### Issue: "User not found in database"
**Solution**:
1. Check user ID spelling (case-sensitive)
2. Verify user was enrolled successfully
3. Check database statistics:
   ```bash
   python main.py
   # Select option 4 to view database
   ```

## Performance Issues

### Issue: Low FPS / Slow processing
**Solutions**:

1. **Reduce camera resolution**:
   ```python
   # In config.py
   CAMERA_WIDTH = 640
   CAMERA_HEIGHT = 480
   ```

2. **Disable visualization**:
   ```python
   DRAW_TESSELATION = False
   DRAW_CONTOURS = False
   DRAW_IRISES = False
   ```

3. **Process every Nth frame**:
   ```python
   # In your code
   frame_count = 0
   if frame_count % 2 == 0:  # Process every 2nd frame
       landmarks = detector.detect(frame)
   frame_count += 1
   ```

## Database Issues

### Issue: Database file corrupted
**Solution**:
```bash
# Backup and reset database
mv biometric_db biometric_db_backup
mkdir biometric_db
# Re-enroll users
```

### Issue: "Permission denied" when saving database
**Solution**:
1. Check folder permissions
2. Run with appropriate permissions
3. Change database path to user directory:
   ```python
   # In config.py
   import os
   DATABASE_PATH = os.path.expanduser("~/biometric_db")
   ```

## Platform-Specific Issues

### Windows

**Issue**: "DLL load failed"
**Solution**:
```bash
pip install --upgrade opencv-python
# Install Visual C++ Redistributable
```

### macOS

**Issue**: Camera permission denied
**Solution**:
- System Preferences → Security & Privacy → Camera
- Enable for Terminal or your IDE

### Linux

**Issue**: "Permission denied: /dev/video0"
**Solution**:
```bash
sudo usermod -a -G video $USER
# Log out and log back in
```

## Testing & Debugging

### Run Installation Test
```bash
python test_installation.py
```

### Enable Debug Mode
```python
# Add to your code
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Test Individual Components
```python
# Test face detection only
from face_mesh_detector import FaceMeshDetector
import cv2

detector = FaceMeshDetector()
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
landmarks = detector.detect(frame)
print(f"Detected: {landmarks is not None}")
```

## Getting Help

If issues persist:

1. Run `python test_installation.py` and share output
2. Check Python version: `python --version` (3.8+ required)
3. Check package versions: `pip list`
4. Review error messages carefully
5. Check README.md for additional information

## Common Error Messages

| Error | Likely Cause | Solution |
|-------|--------------|----------|
| "No module named..." | Package not installed | `pip install <package>` |
| "Camera not accessible" | Camera in use or no permission | Close other apps, check permissions |
| "No face detected" | Poor lighting or positioning | Improve lighting, center face |
| "User not found" | Wrong user ID | Check spelling, view database |
| "Verification failed" | Low similarity | Re-enroll or lower threshold |

---

**Still having issues?** Review the full documentation in README.md or check example_usage.py for working code examples.

