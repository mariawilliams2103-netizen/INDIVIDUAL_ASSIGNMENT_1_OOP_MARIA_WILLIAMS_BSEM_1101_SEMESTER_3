"""Non-interactive demo: shows classes, objects, the dictionary, and all
three method types working together. Run with:  python demo.py
"""

from models import Patient, Vaccine, Vaccination
import tracker

print("=== 1. Object creation and interaction ===")
patients = {}
p1 = tracker.add_patient(patients, "0-1")
p2 = tracker.add_patient(patients, "2-5")
print(f"Created patients: {p1.patient_id}, {p2.patient_id}")
opv = Vaccine.from_code("opv")                      # class method
print("Vaccine from class method:", opv.display_info())
record = p1.add_vaccination(opv, "2026-01-10")      # Patient uses Vaccine
print("Linked record:", record.display_info().strip())

print("\n=== 2. Dictionary: add and display records ===")
tracker.record_vaccination(patients, "P001", "BCG", "2026-01-10")
tracker.record_vaccination(patients, "P002", "MEASLES", "2025-11-05")
tracker.record_vaccination(patients, "P002", "MEASLES", "2099-01-01", "Scheduled")
tracker.display_patients(patients)

print("\n=== 3. Instance, class and static methods ===")
p2.update_record("P002-V02", "Missed")              # instance method
print("After update_record:", p2.vaccinations["P002-V02"].display_info().strip())
print("Patient.total_patients() ->", Patient.total_patients())          # class method
print("Patient.is_valid_id('P001') ->", Patient.is_valid_id("P001"))    # static method
print("Patient.is_valid_id('John Smith') ->", Patient.is_valid_id("John Smith"))
print("Vaccination.parse_date('2026-13-45') ->", Vaccination.parse_date("2026-13-45"))

print("\n=== 4. Friendly error handling ===")
for bad in (lambda: tracker.record_vaccination(patients, "P009", "BCG", "2026-01-01"),
            lambda: tracker.record_vaccination(patients, "P001", "XYZ", "2026-01-01"),
            lambda: tracker.record_vaccination(patients, "P001", "BCG", "2026-01-01")):
    try:
        bad()
    except (ValueError, KeyError) as error:
        print("Problem:", error.args[0])

print("\n=== 5. Coverage summary ===")
tracker.coverage_summary(patients)
