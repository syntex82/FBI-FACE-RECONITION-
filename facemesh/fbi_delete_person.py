"""
Delete a person from FBI database
"""

from fbi_system import FBIFacialRecognitionSystem

print("=" * 70)
print("FBI DATABASE - DELETE PERSON")
print("=" * 70)
print()

system = FBIFacialRecognitionSystem()

# Show current persons
persons = system.database.get_all_persons()
if not persons:
    print("Database is empty - no persons to delete")
    system.close()
    exit(0)

print("Current persons in database:")
for i, person in enumerate(persons, 1):
    print(f"{i}. {person['name']} ({person['person_id']}) - {len(person['images'])} images")

print()
person_id = input("Enter Person ID to delete: ").strip()

if not person_id:
    print("No person ID entered")
    system.close()
    exit(0)

# Delete person
success, message = system.database.delete_person(person_id)

if success:
    print(f"\n✓ {message}")
    
    # Show updated stats
    stats = system.database.get_statistics()
    print(f"\nDatabase Statistics:")
    print(f"  Total Persons: {stats['total_persons']}")
    print(f"  Total Images: {stats['total_images']}")
else:
    print(f"\n✗ {message}")

system.close()

