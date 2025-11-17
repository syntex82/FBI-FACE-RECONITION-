# FBI Database - Quick Start Guide

## 🚀 **Super Easy Method (Recommended)**

### **Add a New Person in 3 Minutes:**

```bash
python quick_add_person.py
```

**That's it!** The script will:
1. ✅ Ask for their details (name, age, occupation, etc.)
2. ✅ Open camera to capture photos
3. ✅ Enroll them in the database
4. ✅ Add their profile automatically

---

## 📸 **Step-by-Step Example:**

### **1. Run the script:**
```bash
python quick_add_person.py
```

### **2. Enter information:**
```
Enter Person ID: sarah_jones
Enter Full Name: Sarah Jones
Enter Age: 28
Enter Gender: Female
Enter Occupation: Police Officer
Enter Nationality: British
```

### **3. Capture photos:**
- Camera opens
- Press **SPACE** to take photos (take 3-5 from different angles)
- Press **Q** when done

### **4. Done!**
```
✓ SUCCESS!
Sarah Jones has been added to the FBI database!
  Person ID: sarah_jones
  Photos: 4
  Status: CLEAR
```

---

## 🎯 **What You Currently Have:**

**People in Database:**
- ✅ Michael Blenkinsop (Age 43, Rigger in Oil and Gas)

**To add more people:**
- Just run `quick_add_person.py` for each person!

---

## 🎮 **Testing the System:**

After adding people, test the FBI app:

```bash
python fbi_app_fixed.py
```

**Controls:**
- **F** - Fullscreen
- **D** - Toggle Dashboard
- **Q** - Quit
- **S** - Show Statistics

**When someone looks at the camera:**
- ✅ Face detected
- ✅ Match found
- ✅ Dashboard shows their complete profile

---

## 📊 **Example Profiles:**

### **Profile 1: Michael Blenkinsop**
```json
{
  "person_id": "michael",
  "full_name": "Michael Blenkinsop",
  "age": 43,
  "gender": "Male",
  "occupation": "Rigger in Oil and Gas",
  "criminal_record": "No Previous Convictions",
  "status": "CLEAR",
  "risk_level": "LOW"
}
```

### **Profile 2: Sarah Jones (Example)**
```json
{
  "person_id": "sarah_jones",
  "full_name": "Sarah Jones",
  "age": 28,
  "gender": "Female",
  "occupation": "Police Officer",
  "criminal_record": "No Previous Convictions",
  "status": "CLEAR",
  "risk_level": "LOW"
}
```

---

## 🔧 **Manual Method (If Needed):**

### **Option A: You Have Photos Already**

1. **Create folder:**
   ```
   enrollment_images/john_doe/
   ```

2. **Put photos in folder:**
   ```
   enrollment_images/john_doe/photo1.jpg
   enrollment_images/john_doe/photo2.jpg
   enrollment_images/john_doe/photo3.jpg
   ```

3. **Enroll:**
   ```bash
   python fbi_enroll.py
   ```
   - Person ID: `john_doe`
   - Name: `John Doe`
   - Consent: `yes`
   - Folder: `enrollment_images/john_doe`

4. **Add profile:**
   - Edit `fbi_profiles.json`
   - Add entry for `john_doe`

### **Option B: Capture Photos First**

1. **Capture:**
   ```bash
   python capture_enrollment_images.py
   ```

2. **Enroll:**
   ```bash
   python fbi_enroll.py
   ```

3. **Add profile:**
   - Edit `fbi_profiles.json`

---

## 📋 **Status Codes:**

| Status | Color | Meaning |
|--------|-------|---------|
| `CLEAR` | 🟢 Green | No issues, approved |
| `WARNING` | 🟡 Yellow | Caution required |
| `DANGER` | 🔴 Red | High risk, alert |

| Risk Level | Meaning |
|------------|---------|
| `LOW` | Standard clearance |
| `MEDIUM` | Requires monitoring |
| `HIGH` | Restricted access |

---

## ✅ **Checklist for Adding Someone:**

- [ ] Run `python quick_add_person.py`
- [ ] Enter their details
- [ ] Capture 3-5 photos (different angles)
- [ ] Wait for enrollment to complete
- [ ] Test with `python fbi_app_fixed.py`
- [ ] Verify their profile shows correctly

---

## 🎯 **Tips for Best Results:**

**Photo Quality:**
- ✅ Good lighting (face clearly visible)
- ✅ Look at camera directly
- ✅ Take from different angles (straight, left, right)
- ✅ No sunglasses or hats
- ✅ 3-5 photos minimum

**Person ID:**
- ✅ Use lowercase
- ✅ Use underscores instead of spaces
- ✅ Make it unique
- ✅ Examples: `john_smith`, `sarah_jones`, `mike_brown`

**Profile Information:**
- ✅ Be accurate
- ✅ Fill in all fields
- ✅ Use proper status codes
- ✅ Add useful notes

---

## 🚀 **Ready to Add Someone?**

**Just run:**
```bash
python quick_add_person.py
```

**That's all you need!** 🎉

---

## 📞 **Need Help?**

**Common Issues:**

**"Camera won't open"**
- Check camera permissions in Windows
- Make sure no other app is using camera
- Try restarting the script

**"No face detected"**
- Make sure face is clearly visible
- Check lighting
- Look directly at camera
- Remove sunglasses/hats

**"Person already exists"**
- Use a different person_id
- Or delete the old entry first

---

**For detailed instructions, see:** `HOW_TO_ADD_PEOPLE.md`

