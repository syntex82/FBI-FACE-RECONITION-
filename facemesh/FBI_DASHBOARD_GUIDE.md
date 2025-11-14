# FBI Dashboard System - User Guide

## 🎯 Quick Start

Run the FBI Dashboard application:
```bash
python fbi_app_dashboard.py
```

---

## 📊 Dashboard Features

### **Automatic Profile Display**
When Michael Blenkinsop is identified, the dashboard **automatically appears** with:

#### **LEFT COLUMN - Personal Information:**
- Full Name: Michael Blenkinsop
- Age: 43
- Gender: Male
- Date of Birth: N/A
- Nationality: British
- Height, Weight, Eye Color, Hair Color, Blood Type

#### **RIGHT COLUMN - Professional & Criminal Record:**
- **Occupation:** Rigger in Oil and Gas
- **Clearance Level:** STANDARD
- **Criminal Record:** No Previous Convictions
- **Status:** CLEAR (green)
- **Risk Level:** LOW

#### **BOTTOM - Match Information:**
- Confidence Score (percentage)
- Match Status (POSITIVE MATCH/NO MATCH)
- Visual confidence meter
- Notes: "Oil and gas industry professional. Clean record."

---

## 🎮 Controls

| Key | Action |
|-----|--------|
| **F** | Toggle Fullscreen (RECOMMENDED) |
| **D** | Toggle Dashboard ON/OFF |
| **Q** | Quit Application |
| **S** | Show Database Statistics |
| **R** | Generate Match Report |

---

## ✨ How It Works

1. **Look at camera** → System detects your face
2. **Match found** → Dashboard automatically appears with complete profile
3. **Press F** → Go fullscreen for best viewing
4. **Press D** → Toggle between live view and dashboard
5. **Move away** → Returns to scanning mode

---

## 🖥️ Display Improvements

### **Fixed Issues:**
- ✅ **Larger canvas** (1920x1080) - no more cramped text
- ✅ **Better spacing** (45px line spacing) - no overlapping
- ✅ **Bigger fonts** (0.7-1.2 scale) - easy to read
- ✅ **Fullscreen support** - press F for full screen
- ✅ **Resizable window** - drag to resize as needed

### **Text Sizes:**
- Section Headers: Large (1.0 scale, bold)
- Info Labels: Medium (0.7 scale)
- Info Values: Medium (0.7 scale)
- Match Info: Extra Large (1.2 scale)

---

## 📝 Profile Data Location

Profiles are stored in: `fbi_profiles.json`

### **Current Profile:**
```json
{
  "michael": {
    "person_id": "michael",
    "full_name": "Michael Blenkinsop",
    "age": 43,
    "gender": "Male",
    "occupation": "Rigger in Oil and Gas",
    "criminal_record": "No Previous Convictions",
    "status": "CLEAR",
    "risk_level": "LOW",
    "nationality": "British",
    "notes": "Oil and gas industry professional. Clean record."
  }
}
```

### **To Add More People:**
1. Edit `fbi_profiles.json`
2. Add new entry with same format
3. Enroll their images using `fbi_enroll.py`
4. System will automatically show their profile when matched

---

## 🎨 Color Coding

- **FBI Gold** (#00D7FF) - Headers, labels
- **Green** - CLEAR status, positive matches
- **Yellow** - WARNING status, instructions
- **Red** - DANGER status, negative matches
- **White** - Data values

---

## 🔧 Troubleshooting

### **Text Still Overlapping?**
- Press **F** for fullscreen
- Resize window larger
- Dashboard is designed for 1920x1080 display

### **Dashboard Not Showing?**
- Make sure you're enrolled in database
- Look directly at camera
- Wait for match (confidence ≥75%)
- Press **D** to manually toggle

### **Can't Read Text?**
- Press **F** for fullscreen mode
- Move closer to screen
- Increase monitor resolution

---

## 📊 Example Output

When you look at the camera, you'll see:

```
╔══════════════════════════════════════════════════════════════╗
║           FBI IDENTIFICATION DASHBOARD                       ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  PERSONAL INFORMATION          PROFESSIONAL INFORMATION      ║
║  ────────────────────          ───────────────────────      ║
║  FULL NAME: Michael Blenkinsop OCCUPATION: Rigger in Oil... ║
║  AGE: 43                       CLEARANCE LEVEL: STANDARD    ║
║  GENDER: Male                                               ║
║  NATIONALITY: British          CRIMINAL RECORD              ║
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
║  NOTES: Oil and gas industry professional. Clean record.    ║
║                                                              ║
║  Press D to toggle | Q to Quit | F for Fullscreen          ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 🚀 Next Steps

1. **Test the system** - Look at camera and verify dashboard appears
2. **Try fullscreen** - Press F for best experience
3. **Add more profiles** - Edit `fbi_profiles.json` to add colleagues
4. **Generate reports** - Press R to create match reports

---

**Enjoy your FBI-style identification dashboard!** 🎉

