# FBI Facial Recognition System

A professional-grade facial recognition system with FBI-style interface, complete profile management, and dashboard display.

![System Status](https://img.shields.io/badge/Status-Operational-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8--3.13-blue)
![License](https://img.shields.io/badge/License-Private-red)

---

## 📋 **Overview**

The FBI Facial Recognition System is a comprehensive biometric identification platform featuring:

- ✅ Real-time face detection and recognition
- ✅ Professional FBI-style dashboard interface
- ✅ Multi-image enrollment for accuracy
- ✅ Complete profile management system
- ✅ Match logging and reporting
- ✅ Confidence scoring and quality assessment
- ✅ Fullscreen display support

**Perfect for:** Security systems, access control, attendance tracking, law enforcement training

---

## 🚀 **Quick Start**

### **1. Installation**

See [`INSTALLATION.md`](INSTALLATION.md) for detailed setup instructions.

**Quick install:**
```bash
# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux

# Install dependencies
pip install opencv-python opencv-contrib-python numpy scikit-learn scipy
```

---

### **2. Add People to Database**
```bash
python quick_add_person.py
```

**This will:**
1. Ask for person details (name, age, occupation, etc.)
2. Open camera to capture photos
3. Automatically enroll them
4. Add their profile
5. Done in 3 minutes!

---

### **3. Run the FBI System**
```bash
python fbi_app_fixed.py
```

**Features:**
- 🎥 Live camera feed with face detection
- 📊 Automatic dashboard when person is matched
- 🖥️ Fullscreen support (press F)
- 📈 Real-time confidence scoring
- 📝 Match logging and reports

**Controls:**
- **F** - Toggle Fullscreen
- **D** - Toggle Dashboard
- **Q** - Quit
- **S** - Show Statistics
- **R** - Generate Report

---

### **4. View Database**
```bash
python view_database.py
```

Shows all enrolled persons with their profiles and statistics.

---

## 📚 **Documentation**

| File | Description |
|------|-------------|
| **[`INSTALLATION.md`](INSTALLATION.md)** | Complete installation guide with system requirements |
| **[`USER_GUIDE.md`](USER_GUIDE.md)** | Comprehensive user manual with all features |
| **[`QUICK_START_GUIDE.md`](QUICK_START_GUIDE.md)** | Quick start guide for beginners |
| **[`HOW_TO_ADD_PEOPLE.md`](HOW_TO_ADD_PEOPLE.md)** | Detailed instructions for adding people |
| **[`FBI_DASHBOARD_GUIDE.md`](FBI_DASHBOARD_GUIDE.md)** | Dashboard features and controls |

**Start here:** [`INSTALLATION.md`](INSTALLATION.md) → [`USER_GUIDE.md`](USER_GUIDE.md)

---

## 🛠️ **Available Tools**

### **Main Applications:**
- `fbi_app_fixed.py` - Main FBI recognition system (bug-free version)
- `fbi_app_dashboard.py` - Original dashboard version
- `fbi_app.py` - Basic version

### **Enrollment Tools:**
- `quick_add_person.py` - ⭐ **EASIEST** - All-in-one enrollment
- `fbi_enroll.py` - Manual enrollment from existing photos
- `capture_enrollment_images.py` - Capture photos only

### **Database Tools:**
- `view_database.py` - View all enrolled persons
- `fbi_delete_person.py` - Remove a person from database

### **Testing Tools:**
- `test_dashboard.py` - Test dashboard rendering
- `fbi_demo_no_camera.py` - Demo without camera

---

## 📊 **System Architecture**

### **Core Modules:**
- `fbi_system.py` - Main system integration
- `fbi_database.py` - Database management
- `fbi_matcher.py` - Face matching engine
- `fbi_dashboard.py` - Dashboard display
- `fbi_ui.py` - UI components
- `fbi_logger.py` - Logging and reports

### **Data Files:**
- `fbi_database/metadata.json` - Person metadata
- `fbi_database/features.pkl` - Biometric features
- `fbi_profiles.json` - Profile information
- `fbi_logs/` - Match logs and reports

---

## 🎯 **How It Works**

### **1. Enrollment Process:**
```
Capture Photos → Extract Features → Store in Database → Add Profile
```

### **2. Recognition Process:**
```
Camera Feed → Detect Face → Extract Features → Match Against Database → Show Dashboard
```

### **3. Matching Algorithm:**
- Extracts 22 geometric features from face
- Compares against all enrolled images
- Uses cosine similarity scoring
- Threshold: ≥75% = POSITIVE MATCH

---

## 📸 **Photo Requirements**

**For Best Results:**
- ✅ 3-5 photos per person
- ✅ Different angles (straight, left, right)
- ✅ Good lighting
- ✅ Face clearly visible
- ✅ No sunglasses or hats
- ✅ Look at camera

---

## 🎨 **Dashboard Features**

When a person is matched, the dashboard shows:

### **Personal Information:**
- Full Name
- Age, Gender
- Nationality
- Physical characteristics

### **Professional Information:**
- Occupation
- Clearance Level
- Employment details

### **Security Information:**
- Criminal Record
- Status (CLEAR/WARNING/DANGER)
- Risk Level (LOW/MEDIUM/HIGH)
- Match Confidence

### **Visual Elements:**
- FBI-style header
- Color-coded status indicators
- Confidence meter
- Professional layout

---

## 🔧 **Configuration**

### **Status Codes:**
- `CLEAR` 🟢 - No issues, approved
- `WARNING` 🟡 - Caution required
- `DANGER` 🔴 - High risk, alert

### **Risk Levels:**
- `LOW` - Standard clearance
- `MEDIUM` - Requires monitoring
- `HIGH` - Restricted access

### **Clearance Levels:**
- `STANDARD` - Basic access
- `CONFIDENTIAL` - Sensitive access
- `SECRET` - High-level access
- `TOP SECRET` - Maximum clearance

---

## 📝 **Example Workflow**

### **Adding a New Person:**

1. **Run enrollment tool:**
   ```bash
   python quick_add_person.py
   ```

2. **Enter details:**
   ```
   Person ID: sarah_jones
   Full Name: Sarah Jones
   Age: 28
   Gender: Female
   Occupation: Police Officer
   Nationality: British
   ```

3. **Capture photos:**
   - Camera opens
   - Press SPACE 3-5 times
   - Press Q when done

4. **Done!**
   ```
   ✓ SUCCESS!
   Sarah Jones has been added to the FBI database!
   ```

5. **Test it:**
   ```bash
   python fbi_app_fixed.py
   ```

---

## 🎯 **Current Database**

Run `python view_database.py` to see:

```
DATABASE STATISTICS
----------------------------------------------------------------------
Total Persons: 1
Total Images: 1
Avg Images/Person: 1.0

ENROLLED PERSONS
======================================================================

┌─ PERSON ID: michael
│
│  Name: Michael Blenkinsop
│  Images: 1
│  Enrolled: 2025-11-14
│  Consent: Yes
│
│  ┌─ PROFILE INFORMATION
│  │  Age: 43
│  │  Gender: Male
│  │  Occupation: Rigger in Oil and Gas
│  │  Status: 🟢 CLEAR
│  │  Risk Level: LOW
│  └─
└─
```

---

## 🚀 **Next Steps**

1. **Add more people:** `python quick_add_person.py`
2. **Test the system:** `python fbi_app_fixed.py`
3. **View database:** `python view_database.py`
4. **Generate reports:** Press R in the app

---

## 📞 **Support**

**Common Issues:**
- Camera won't open → Check Windows permissions
- No face detected → Better lighting, look at camera
- Person already exists → Use different person_id

**For detailed help, see:**
- `QUICK_START_GUIDE.md`
- `HOW_TO_ADD_PEOPLE.md`

---

**System Status:** ✅ **OPERATIONAL**

**Ready to use!** 🎉

