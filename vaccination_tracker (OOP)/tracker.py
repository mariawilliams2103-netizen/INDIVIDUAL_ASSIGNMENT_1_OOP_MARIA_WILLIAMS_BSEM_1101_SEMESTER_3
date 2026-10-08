"""Functions that manage the collection of patients.

The single data structure is a dictionary: patient_id -> Patient.
"""

from models import AGE_GROUPS, VACCINE_CATALOGUE, Patient, Vaccine


def next_patient_id(patients):
    """Generate the next anonymous ID (P001, P002, ...). No personal data used."""
    return f"P{len(patients) + 1:03d}"


def add_patient(patients, age_group):
    """Task 2 function: add a new Patient to the dictionary and return it."""
    patient = Patient(next_patient_id(patients), age_group)
    patients[patient.patient_id] = patient
    return patient


def display_patients(patients):
    """Task 2 function: print every patient in the dictionary."""
    if not patients:
        print("No patients registered yet.")
        return
    for patient in patients.values():
        print(patient.display_info())
        print("-" * 50)
    print(f"Total patients: {Patient.total_patients()}")


def record_vaccination(patients, patient_id, vaccine_code, date_given, status="Completed"):
    """Link a Vaccine to a Patient by recording a dose (object interaction)."""
    patient = patients.get(patient_id.strip().upper())
    if patient is None:
        raise KeyError(f"Patient '{patient_id}' was not found.")
    vaccine = Vaccine.from_code(vaccine_code)
    if vaccine is None:
        codes = ", ".join(code for code, _, _ in VACCINE_CATALOGUE)
        raise ValueError(f"Unknown vaccine code. Choose one of: {codes}")
    return patient.add_vaccination(vaccine, date_given, status)


def coverage_summary(patients):
    """Print how many patients are fully vaccinated against each vaccine."""
    total = len(patients)
    print(f"Coverage summary ({total} patient(s))")
    for code, disease, doses in VACCINE_CATALOGUE:
        vaccine = Vaccine(code, disease, doses)
        done = sum(1 for p in patients.values() if p.is_fully_vaccinated(vaccine))
        percent = (done / total * 100) if total else 0
        print(f"  {code:<8} {done}/{total} fully vaccinated ({percent:.0f}%)")


def load_demo_data(patients):
    """Add anonymous sample data so the program can be tried straight away."""
    first = add_patient(patients, "0-1")
    second = add_patient(patients, "2-5")
    third = add_patient(patients, "18-59")
    record_vaccination(patients, first.patient_id, "BCG", "2026-01-10")
    record_vaccination(patients, first.patient_id, "OPV", "2026-01-10")
    record_vaccination(patients, first.patient_id, "OPV", "2026-03-12")
    record_vaccination(patients, second.patient_id, "MEASLES", "2025-11-05")
    record_vaccination(patients, second.patient_id, "MEASLES", "2025-12-05")
    record_vaccination(patients, third.patient_id, "COVID19", "2026-02-01")
    record_vaccination(patients, third.patient_id, "COVID19", "2099-01-01", "Scheduled")
    return patients


def age_group_menu_text():
    return "  ".join(f"{i}) {group}" for i, group in enumerate(AGE_GROUPS, start=1))
