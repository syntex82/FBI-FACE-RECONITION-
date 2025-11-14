# FBI Facial Recognition System - Installation Guide

## 📋 **System Requirements**

### **Operating System:**
- ✅ Windows 10/11 (Tested and working)
- ✅ macOS 10.14+
- ✅ Linux (Ubuntu 18.04+, Debian, Fedora)

### **Hardware Requirements:**
- **CPU:** Intel Core i5 or equivalent (minimum)
- **RAM:** 4GB minimum, 8GB recommended
- **Storage:** 500MB free space
- **Camera:** Webcam or USB camera (required for face detection)
- **Display:** 1920x1080 recommended for best dashboard experience

### **Software Requirements:**
- **Python:** 3.8 - 3.13 (Python 3.13.6 tested and working)
- **pip:** Latest version
- **Git:** For cloning repository (optional)

---

## 🚀 **Installation Steps**

### **Step 1: Install Python**

#### **Windows:**
1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run installer
3. ✅ **IMPORTANT:** Check "Add Python to PATH"
4. Click "Install Now"
5. Verify installation:
   ```bash
   python --version
   ```
   Should show: `Python 3.13.6` (or your version)

#### **macOS:**
```bash
# Using Homebrew
brew install python@3.13

# Verify
python3 --version
```

#### **Linux:**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv

# Fedora
sudo dnf install python3 python3-pip

# Verify
python3 --version
```

---

### **Step 2: Set Up Project**

#### **Option A: If you have the files already**
```bash
# Navigate to project folder
cd C:\Users\micky\OneDrive\Desktop\facemesh

# Or on macOS/Linux
cd ~/facemesh
```

#### **Option B: If starting fresh**
```bash
# Create project folder
mkdir fbi-facial-recognition
cd fbi-facial-recognition

# Copy all project files here
```

---

### **Step 3: Create Virtual Environment**

#### **Windows:**
```bash
# Create virtual environment
python -m venv .venv

# Activate it
.venv\Scripts\activate

# You should see (.venv) in your prompt
```

#### **macOS/Linux:**
```bash
# Create virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate

# You should see (.venv) in your prompt
```

---

### **Step 4: Install Dependencies**

```bash
# Make sure virtual environment is activated (you should see .venv in prompt)

# Install required packages
pip install opencv-python==4.12.0.88
pip install opencv-contrib-python==4.12.0.88
pip install numpy==2.2.6
pip install scikit-learn==1.7.2
pip install scipy==1.16.3

# Verify installation
pip list
```

**Expected output:**
```
Package                Version
---------------------- -------
numpy                  2.2.6
opencv-contrib-python  4.12.0.88
opencv-python          4.12.0.88
scikit-learn           1.7.2
scipy                  1.16.3
```

---

### **Step 5: Create Required Folders**

```bash
# Windows
mkdir fbi_database
mkdir fbi_database\images
mkdir fbi_logs
mkdir enrollment_images

# macOS/Linux
mkdir -p fbi_database/images
mkdir -p fbi_logs
mkdir -p enrollment_images
```

---

### **Step 6: Verify Installation**

```bash
# Test Python imports
python -c "import cv2; import numpy; import sklearn; print('✓ All packages installed correctly')"
```

**Expected output:**
```
✓ All packages installed correctly
```

---

### **Step 7: Test Camera Access**

```bash
# Run camera test
python -c "import cv2; cap = cv2.VideoCapture(0); print('✓ Camera working' if cap.isOpened() else '✗ Camera not accessible'); cap.release()"
```

**Expected output:**
```
✓ Camera working
```

**If camera doesn't work:**
- **Windows:** Check camera permissions in Settings → Privacy → Camera
- **macOS:** Grant terminal camera access in System Preferences → Security & Privacy
- **Linux:** Check if user is in `video` group: `sudo usermod -a -G video $USER`

---

## ✅ **Installation Complete!**

Your system is now ready to use!

### **Quick Test:**

```bash
# View current database
python view_database.py

# Add yourself to the database
python quick_add_person.py

# Run the FBI system
python fbi_app_fixed.py
```

---

## 🔧 **Troubleshooting**

### **Problem: "python: command not found"**
**Solution:**
- Windows: Use `py` instead of `python`
- macOS/Linux: Use `python3` instead of `python`

### **Problem: "No module named 'cv2'"**
**Solution:**
```bash
# Make sure virtual environment is activated
# You should see (.venv) in your prompt

# Reinstall OpenCV
pip install --upgrade opencv-python opencv-contrib-python
```

### **Problem: "Permission denied" on Linux/macOS**
**Solution:**
```bash
# Don't use sudo with pip in virtual environment
# Make sure .venv is activated first
source .venv/bin/activate
pip install opencv-python
```

### **Problem: Camera not working**
**Solution:**
- Close other apps using camera (Zoom, Teams, etc.)
- Check camera permissions in OS settings
- Try different camera index: Edit code to use `cv2.VideoCapture(1)` instead of `0`

### **Problem: "ImportError: DLL load failed" (Windows)**
**Solution:**
```bash
# Install Visual C++ Redistributable
# Download from: https://aka.ms/vs/17/release/vc_redist.x64.exe
```

---

## 📦 **Package Details**

| Package | Version | Purpose |
|---------|---------|---------|
| opencv-python | 4.12.0.88 | Face detection, image processing |
| opencv-contrib-python | 4.12.0.88 | Additional OpenCV features |
| numpy | 2.2.6 | Numerical operations, arrays |
| scikit-learn | 1.7.2 | Machine learning, similarity metrics |
| scipy | 1.16.3 | Scientific computing |

**Total size:** ~150MB

---

## 🔄 **Updating the System**

```bash
# Activate virtual environment
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux

# Update packages
pip install --upgrade opencv-python opencv-contrib-python numpy scikit-learn scipy
```

---

## 🗑️ **Uninstallation**

```bash
# Deactivate virtual environment
deactivate

# Delete project folder
# Windows
rmdir /s facemesh

# macOS/Linux
rm -rf facemesh
```

---

## 📞 **Need Help?**

**Common Issues:**
1. Virtual environment not activating → Make sure you're in project folder
2. Packages not installing → Update pip: `pip install --upgrade pip`
3. Camera not working → Check OS permissions
4. Import errors → Reinstall packages in virtual environment

**Next Steps:**
- See `USER_GUIDE.md` for how to use the system
- See `QUICK_START_GUIDE.md` for adding people
- See `README_FBI_SYSTEM.md` for complete documentation

---

**Installation Status:** ✅ **READY TO USE**

