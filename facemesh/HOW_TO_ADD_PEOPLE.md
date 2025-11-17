# How to Add People to the FBI Database

There are **3 easy ways** to add people to the FBI database:

---

## 🎯 **Method 1: Quick Enrollment Tool (EASIEST)**

### **Step 1: Capture Photos**
```bash
python capture_enrollment_images.py
```

**What it does:**
- Opens your camera
- Press **SPACE** to capture photos (take 3-5 photos from different angles)
- Press **Q** when done
- Saves photos to `enrollment_images/[person_id]/`

**Tips for good photos:**
- Look straight at camera
- Turn head slightly left/right
- Good lighting
- No sunglasses or hats
- 3-5 photos is ideal

---

### **Step 2: Enroll the Person**
```bash
python fbi_enroll.py
```

**You'll be asked:**
1. **Person ID:** Unique identifier (e.g., `john_smith`, `jane_doe`)
2. **Person Name:** Full name (e.g., `John Smith`)
3. **Consent:** Type `yes` (required)
4. **Folder path:** Type `enrollment_images/[person_id]`

**Example:**
```
Enter Person ID: john_smith
Enter Person Name: John Smith
Has consent been obtained? yes
Enter path to folder: enrollment_images/john_smith

Found 4 images
Processing...
✓ Successfully enrolled John Smith with 4 images
```

---

### **Step 3: Add Profile Information**

Edit `fbi_profiles.json` and add their details:

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
  },
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

**Important:** Make sure the `person_id` matches what you used in enrollment!

---

## 🚀 **Method 2: Quick Script (FASTEST)**

I'll create a super-easy script for you that does everything in one go!

```bash
python quick_add_person.py
```

This will:
1. Ask for person details
2. Capture photos automatically
3. Enroll them
4. Add profile information
5. All done!

---

## 📁 **Method 3: Manual (ADVANCED)**

If you already have photos:

1. **Create folder structure:**
   ```
   enrollment_images/
   ├── person1/
   │   ├── photo1.jpg
   │   ├── photo2.jpg
   │   └── photo3.jpg
   └── person2/
       ├── photo1.jpg
       └── photo2.jpg
   ```

2. **Run enrollment:**
   ```bash
   python fbi_enroll.py
   ```

3. **Add profile to `fbi_profiles.json`**

---

## 📋 **Profile Fields Explained**

| Field | Description | Example |
|-------|-------------|---------|
| `person_id` | Unique ID (must match enrollment) | `"john_smith"` |
| `full_name` | Full legal name | `"John Smith"` |
| `age` | Age in years | `35` |
| `gender` | Gender | `"Male"` / `"Female"` |
| `occupation` | Job/profession | `"Software Engineer"` |
| `criminal_record` | Criminal history | `"No Previous Convictions"` |
| `status` | Current status | `"CLEAR"` / `"WARNING"` / `"DANGER"` |
| `risk_level` | Risk assessment | `"LOW"` / `"MEDIUM"` / `"HIGH"` |
| `nationality` | Country | `"American"` |
| `notes` | Additional info | Any text |

**Optional fields:**
- `date_of_birth`: `"1990-01-15"`
- `height`: `"6'2\""`
- `weight`: `"180 lbs"`
- `eye_color`: `"Blue"`
- `hair_color`: `"Brown"`
- `blood_type`: `"O+"`
- `clearance_level`: `"STANDARD"` / `"CONFIDENTIAL"` / `"SECRET"`

---

## ✅ **Verification**

After adding someone, verify they're in the database:

```bash
python fbi_app_fixed.py
```

Then press **S** to see statistics:
```
STATISTICS
==================================================
  Total Persons: 2
  Total Images: 6
  Avg Images/Person: 3.0
==================================================
```

---

## 🎯 **Quick Reference**

**To add a new person:**
1. `python capture_enrollment_images.py` → Capture photos
2. `python fbi_enroll.py` → Enroll them
3. Edit `fbi_profiles.json` → Add profile
4. `python fbi_app_fixed.py` → Test it!

---

## 🔍 **Troubleshooting**

**"Person already exists"**
- Delete them first: Edit `fbi_database/metadata.json` and remove their entry
- Or use a different `person_id`

**"No images found"**
- Check folder path is correct
- Make sure images are .jpg, .png, or .jpeg
- Check images are in the right folder

**"No face detected"**
- Use photos with clear, visible faces
- Good lighting
- Face looking at camera
- No sunglasses or masks

---

**Want me to create the super-easy `quick_add_person.py` script that does everything automatically?** 🚀

