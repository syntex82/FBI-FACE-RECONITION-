"""
FBI Database Viewer
View all people in the database with their profiles
"""

import json
import os
from fbi_system import FBIFacialRecognitionSystem


def view_database():
    """View all people in the database."""
    print("=" * 70)
    print("FBI DATABASE VIEWER")
    print("=" * 70)
    print()
    
    # Load database
    system = FBIFacialRecognitionSystem()
    stats = system.get_database_stats()
    
    print("DATABASE STATISTICS")
    print("-" * 70)
    print(f"Total Persons: {stats.get('total_persons', 0)}")
    print(f"Total Images: {stats.get('total_images', 0)}")
    print(f"Avg Images/Person: {stats.get('avg_images_per_person', 0):.1f}")
    print()
    
    # Load profiles
    profiles_file = "fbi_profiles.json"
    if os.path.exists(profiles_file):
        with open(profiles_file, 'r') as f:
            profiles = json.load(f)
    else:
        profiles = {}
    
    # Get all persons from database
    metadata_file = os.path.join("fbi_database", "metadata.json")
    if os.path.exists(metadata_file):
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)
    else:
        metadata = {}

    # Extract persons from metadata
    persons = metadata.get('persons', {})

    if not persons:
        print("Database is empty. No persons enrolled.")
        print("\nTo add someone, run:")
        print("  python quick_add_person.py")
        system.close()
        return

    print("ENROLLED PERSONS")
    print("=" * 70)
    print()

    for person_id, person_data in persons.items():
        # Skip non-person entries (stats, etc.)
        if not isinstance(person_data, dict):
            continue

        # Skip if no name (invalid entry)
        if 'name' not in person_data:
            continue

        print(f"┌─ PERSON ID: {person_id}")
        print(f"│")

        # Basic info from database
        print(f"│  Name: {person_data.get('name', 'N/A')}")
        print(f"│  Images: {len(person_data.get('images', []))}")
        print(f"│  Enrolled: {person_data.get('created_at', 'N/A')}")
        print(f"│  Consent: {'Yes' if person_data.get('consent_obtained') else 'No'}")
        
        # Profile info if available
        if person_id in profiles:
            profile = profiles[person_id]
            print(f"│")
            print(f"│  ┌─ PROFILE INFORMATION")
            print(f"│  │  Age: {profile.get('age', 'N/A')}")
            print(f"│  │  Gender: {profile.get('gender', 'N/A')}")
            print(f"│  │  Occupation: {profile.get('occupation', 'N/A')}")
            print(f"│  │  Nationality: {profile.get('nationality', 'N/A')}")
            print(f"│  │  Criminal Record: {profile.get('criminal_record', 'N/A')}")
            
            # Status with color indicator
            status = profile.get('status', 'UNKNOWN')
            if status == 'CLEAR':
                status_icon = '🟢'
            elif status == 'WARNING':
                status_icon = '🟡'
            else:
                status_icon = '🔴'
            
            print(f"│  │  Status: {status_icon} {status}")
            print(f"│  │  Risk Level: {profile.get('risk_level', 'N/A')}")
            
            if profile.get('notes'):
                print(f"│  │  Notes: {profile.get('notes')}")
            print(f"│  └─")
        else:
            print(f"│")
            print(f"│  ⚠️  No profile information available")
            print(f"│  Add profile to fbi_profiles.json")
        
        print(f"└─")
        print()
    
    system.close()
    
    print("=" * 70)
    print("\nCOMMANDS:")
    print("  python quick_add_person.py    - Add a new person")
    print("  python fbi_app_fixed.py       - Run FBI recognition system")
    print("  python view_database.py       - View this list again")
    print()


def export_database():
    """Export database to text file."""
    print("\n" + "=" * 70)
    print("EXPORTING DATABASE")
    print("=" * 70)
    
    output_file = f"database_export_{os.path.basename(os.getcwd())}_{os.path.splitext(os.path.basename(__file__))[0]}.txt"
    
    # Redirect print to file
    import sys
    original_stdout = sys.stdout
    
    with open(output_file, 'w') as f:
        sys.stdout = f
        view_database()
    
    sys.stdout = original_stdout
    
    print(f"✓ Database exported to: {output_file}")
    print()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--export':
        export_database()
    else:
        view_database()
        
        # Ask if they want to export
        export = input("Export to file? (y/n): ").strip().lower()
        if export in ['y', 'yes']:
            export_database()

