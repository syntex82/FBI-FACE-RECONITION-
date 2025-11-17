# FBI Facial Recognition System - User Guide

## 📖 **Table of Contents**

1. [Getting Started](#getting-started)
2. [Adding People to Database](#adding-people-to-database)
3. [Running the FBI System](#running-the-fbi-system)
4. [Using the Dashboard](#using-the-dashboard)
5. [Managing the Database](#managing-the-database)
6. [Reports and Logs](#reports-and-logs)
7. [Tips and Best Practices](#tips-and-best-practices)

---

## 🚀 **Getting Started**

### **First Time Setup**

1. **Check Installation:**
   ```bash
   python view_database.py
   ```
   This shows your current database (should be empty if first time)

2. **Add Yourself:**
   ```bash
   python quick_add_person.py
   ```
   Follow the prompts to add yourself to the database

3. **Test the System:**
   ```bash
   python fbi_app_fixed.py
   ```
   Look at the camera - you should be recognized!

---

## 👥 **Adding People to Database**

### **Method 1: Quick Add (Recommended)**

**Best for:** Adding new people with camera

```bash
python quick_add_person.py
```

**Steps:**
1. Enter person details:
   - Person ID (e.g., `john_smith`)
   - Full Name (e.g., `John Smith`)
   - Age (e.g., `35`)
   - Gender (e.g., `Male`)
   - Occupation (e.g., `Software Engineer`)
   - Nationality (e.g., `American`)

2. Camera opens automatically
3. Press **SPACE** to capture photos (take 3-5 from different angles)
4. Press **Q** when done
5. System automatically enrolls them
6. Done!

**Example:**
```
Enter Person ID: sarah_jones
Enter Full Name: Sarah Jones
Enter Age: 28
Enter Gender: Female
Enter Occupation: Police Officer
Enter Nationality: British

[Camera opens - capture 4 photos]

✓ SUCCESS!
Sarah Jones has been added to the FBI database!
```

---

### **Method 2: Manual Enrollment**

**Best for:** When you already have photos

**Step 1: Organize Photos**
```
enrollment_images/
└── john_smith/
    ├── photo1.jpg
    ├── photo2.jpg
    └── photo3.jpg
```

**Step 2: Run Enrollment**
```bash
python fbi_enroll.py
```

**Step 3: Enter Details**
```
Enter Person ID: john_smith
Enter Person Name: John Smith
Has consent been obtained? yes
Enter path to folder: enrollment_images/john_smith
```

**Step 4: Add Profile**
Edit `fbi_profiles.json` and add:
```json
{
  "john_smith": {
    "person_id": "john_smith",
    "full_name": "John Smith",
    "age": 35,
    "gender": "Male",
    "occupation": "Software Engineer",
    "criminal_record": "No Previous Convictions",
    "status": "CLEAR",
    "risk_level": "LOW",
    "nationality": "American",
    "notes": "Tech professional. Clean background."
  }
}
```

---

### **Method 3: Capture Photos Only**

**Best for:** Taking photos now, enrolling later

```bash
python capture_enrollment_images.py
```

**Steps:**
1. Enter person ID
2. Camera opens
3. Press **SPACE** to capture photos
4. Press **Q** when done
5. Photos saved to `enrollment_images/[person_id]/`
6. Enroll later using Method 2

---

## 🎮 **Running the FBI System**

### **Start the System**

```bash
python fbi_app_fixed.py
```

**What You'll See:**
```
======================================================================
FBI FACIAL RECOGNITION SYSTEM
======================================================================

Controls:
  F - Toggle Fullscreen
  D - Toggle Dashboard
  Q - Quit
  S - Statistics
  R - Report

Initializing camera...
✓ Ready!
```

---

### **Keyboard Controls**

| Key | Function | Description |
|-----|----------|-------------|
| **F** | Fullscreen | Toggle fullscreen mode (recommended!) |
| **D** | Dashboard | Toggle dashboard display on/off |
| **Q** | Quit | Exit the application |
| **S** | Statistics | Show database statistics in console |
| **R** | Report | Generate and save match report |

---

### **System Modes**

#### **1. Live View Mode**
- Shows camera feed
- Detects faces in real-time
- Displays match status
- Shows confidence scores

#### **2. Dashboard Mode**
- Automatically appears when person is matched
- Shows complete profile information
- Displays match confidence
- Color-coded status indicators

---

## 📊 **Using the Dashboard**

### **Dashboard Layout**

When someone is recognized, the dashboard shows:

```
╔══════════════════════════════════════════════════════════════╗
║           FBI IDENTIFICATION DASHBOARD                       ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  PERSONAL INFORMATION          PROFESSIONAL INFORMATION      ║
║  ────────────────────          ───────────────────────      ║
║  FULL NAME: John Smith         OCCUPATION: Software Engineer║
║  AGE: 35                       CLEARANCE LEVEL: STANDARD    ║
║  GENDER: Male                                               ║
║  NATIONALITY: American         CRIMINAL RECORD              ║
║                                ───────────────              ║
║                                No Previous Convictions      ║
║                                STATUS: CLEAR                ║
║                                RISK LEVEL: LOW              ║
║                                                              ║
║  MATCH INFORMATION                                          ║
║  ─────────────────                                          ║
║  CONFIDENCE: 92.5%                                          ║
║  STATUS: POSITIVE MATCH                                     ║
║                                                              ║
║  Press D to toggle | Q to Quit | F for Fullscreen          ║
╚══════════════════════════════════════════════════════════════╝
```

---

### **Dashboard Sections**

#### **Left Column - Personal Information:**
- Full Name
- Age
- Gender
- Date of Birth
- Nationality
- Height, Weight
- Eye Color, Hair Color
- Blood Type

#### **Right Column - Professional & Security:**
- Occupation
- Clearance Level
- Criminal Record
- Status (CLEAR/WARNING/DANGER)
- Risk Level (LOW/MEDIUM/HIGH)

#### **Bottom - Match Information:**
- Confidence Score (percentage)
- Match Status (POSITIVE/NEGATIVE)
- Visual confidence meter
- Notes and additional information

---

### **Status Indicators**

| Status | Color | Meaning |
|--------|-------|---------|
| 🟢 CLEAR | Green | No issues, approved for access |
| 🟡 WARNING | Yellow | Caution required, review needed |
| 🔴 DANGER | Red | High risk, deny access |

| Risk Level | Description |
|------------|-------------|
| LOW | Standard clearance, no restrictions |
| MEDIUM | Requires monitoring, limited access |
| HIGH | Restricted access, high security |

---

## 🗄️ **Managing the Database**

### **View Database**

```bash
python view_database.py
```

**Shows:**
- Total persons enrolled
- Total images
- Average images per person
- Complete list of all persons with profiles

**Example Output:**
```
DATABASE STATISTICS
----------------------------------------------------------------------
Total Persons: 3
Total Images: 12
Avg Images/Person: 4.0

ENROLLED PERSONS
======================================================================

┌─ PERSON ID: michael
│  Name: Michael Blenkinsop
│  Images: 4
│  Status: 🟢 CLEAR
│  Occupation: Rigger in Oil and Gas
└─

┌─ PERSON ID: sarah_jones
│  Name: Sarah Jones
│  Images: 4
│  Status: 🟢 CLEAR
│  Occupation: Police Officer
└─
```

---

### **Export Database**

```bash
python view_database.py --export
```

Creates a text file with complete database listing.

---

### **Delete a Person**

```bash
python fbi_delete_person.py
```

**Steps:**
1. Enter person ID to delete
2. Confirm deletion
3. Person removed from database

**Warning:** This cannot be undone!

---

## 📝 **Reports and Logs**

### **Generate Match Report**

**While FBI app is running:**
1. Press **R** key
2. Report saved to `fbi_logs/report_[timestamp].txt`

**Report includes:**
- Database statistics
- Recent matches (last 20)
- Match confidence scores
- Timestamps
- Person details

---

### **Log Files**

**Location:** `fbi_logs/`

**Files:**
- `events.json` - System events log
- `matches.json` - All face matches
- `matches.csv` - Match data in CSV format
- `report_*.txt` - Generated reports

---

### **View Recent Matches**

```bash
# View matches.json
cat fbi_logs/matches.json

# Or open in text editor
notepad fbi_logs/matches.json  # Windows
open fbi_logs/matches.json     # macOS
```

---

## 💡 **Tips and Best Practices**

### **For Best Recognition:**

✅ **Photo Quality:**
- Take 3-5 photos per person
- Use different angles (straight, left, right)
- Good lighting (face clearly visible)
- No sunglasses, hats, or masks
- Look directly at camera

✅ **Camera Setup:**
- Position camera at eye level
- Distance: 2-3 feet from camera
- Avoid backlighting
- Clean camera lens

✅ **Environment:**
- Good room lighting
- Avoid shadows on face
- Neutral background preferred

---

### **Profile Management:**

✅ **Person IDs:**
- Use lowercase
- Use underscores instead of spaces
- Make them unique and memorable
- Examples: `john_smith`, `sarah_j`, `mike_brown`

✅ **Profile Information:**
- Be accurate and complete
- Update regularly
- Use proper status codes
- Add useful notes

---

### **Security Best Practices:**

✅ **Consent:**
- Always obtain consent before enrolling
- Document consent in notes
- Respect privacy

✅ **Data Protection:**
- Keep database secure
- Regular backups
- Limit access to authorized users

✅ **Regular Maintenance:**
- Review profiles monthly
- Update outdated information
- Remove inactive persons
- Check log files

---

## 🎯 **Common Workflows**

### **Daily Use:**
1. Start system: `python fbi_app_fixed.py`
2. Press **F** for fullscreen
3. System automatically recognizes people
4. Dashboard shows when matched
5. Press **Q** to quit

### **Adding New Employee:**
1. Run: `python quick_add_person.py`
2. Enter their details
3. Capture 4-5 photos
4. Test: `python fbi_app_fixed.py`
5. Verify they're recognized

### **Weekly Review:**
1. View database: `python view_database.py`
2. Check match logs: `fbi_logs/matches.json`
3. Generate report: Press **R** in app
4. Update profiles if needed

---

## 📞 **Getting Help**

**Documentation:**
- `INSTALLATION.md` - Installation instructions
- `QUICK_START_GUIDE.md` - Quick start guide
- `HOW_TO_ADD_PEOPLE.md` - Detailed enrollment guide
- `README_FBI_SYSTEM.md` - Complete system overview

**Common Issues:**
- Camera not working → Check permissions
- No match found → Retake photos with better lighting
- Low confidence → Add more photos from different angles

---

**System Status:** ✅ **OPERATIONAL**

**Ready to use!** 🎉

