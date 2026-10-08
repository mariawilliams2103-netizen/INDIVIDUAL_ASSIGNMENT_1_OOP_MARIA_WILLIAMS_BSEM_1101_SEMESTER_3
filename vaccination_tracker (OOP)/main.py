from models import AGE_GROUPS, STATUSES, VACCINE_CATALOGUE
import tracker

MENU = """
=== Vaccination Tracker ===
1. Register new patient (anonymous ID is created for you)
2. Record a vaccination for a patient
3. Update the status of a vaccination record
4. View one patient
5. View all patients
6. Coverage summary
7. Load demo data
8. Show available vaccines
0. Exit
"""


def ask(prompt):
    return input(prompt).strip()


def choose_age_group():
    print("Choose age group:  " + tracker.age_group_menu_text())
    choice = ask("Enter number: ")
    if choice.isdigit() and 1 <= int(choice) <= len(AGE_GROUPS):
        return AGE_GROUPS[int(choice) - 1]
    raise ValueError(f"Please enter a number from 1 to {len(AGE_GROUPS)}.")


def show_vaccines():
    print("Available vaccines:")
    for code, disease, doses in VACCINE_CATALOGUE:
        print(f"  {code:<8} {disease} ({doses} dose(s))")


def run():
    patients = {}   # the single data structure: patient_id -> Patient
    while True:
        print(MENU)
        choice = ask("Choose an option (0-8): ")
        try:
            if choice == "1":
                patient = tracker.add_patient(patients, choose_age_group())
                print(f"Registered. Patient ID: {patient.patient_id}")
            elif choice == "2":
                show_vaccines()
                record = tracker.record_vaccination(
                    patients,
                    ask("Patient ID (e.g. P001): "),
                    ask("Vaccine code: "),
                    ask("Date given (YYYY-MM-DD): "),
                    ask(f"Status ({'/'.join(STATUSES)}): ").capitalize() or "Completed",
                )
                print(f"Saved record {record.record_id}.")
            elif choice == "3":
                patient = patients.get(ask("Patient ID (e.g. P001): ").upper())
                if patient is None:
                    raise KeyError("Patient not found.")
                print(patient.display_info())
                record = patient.update_record(
                    ask("Record ID to update: ").upper(),
                    ask(f"New status ({'/'.join(STATUSES)}): ").capitalize(),
                )
                print(f"Updated {record.record_id} to {record.status}.")
            elif choice == "4":
                patient = patients.get(ask("Patient ID (e.g. P001): ").upper())
                print(patient.display_info() if patient else "Patient not found.")
            elif choice == "5":
                tracker.display_patients(patients)
            elif choice == "6":
                tracker.coverage_summary(patients)
            elif choice == "7":
                tracker.load_demo_data(patients)
                print("Demo data loaded.")
            elif choice == "8":
                show_vaccines()
            elif choice == "0":
                print("Goodbye.")
                break
            else:
                print("\033[91m" + "Please choose a number from the menu (0-8)" + "\033[0m")
        except (ValueError, KeyError) as error:
            print(f"Problem: {error.args[0]}")


if __name__ == "__main__":
    run()
