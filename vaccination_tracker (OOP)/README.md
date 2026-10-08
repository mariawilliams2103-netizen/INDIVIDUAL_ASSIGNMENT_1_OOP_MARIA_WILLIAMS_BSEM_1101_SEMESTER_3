# Vaccination Tracker

A simple, open-source Python program that helps a health clinic record and follow
vaccinations **without storing any personal data**. It was built for
**PROG211 Object-Oriented Programming 1** (Limkokwing University of Creative
Technology, Sierra Leone) as a Digital Public Good (DPG) in the **Health** domain.

- **Author:** Maria Williams, 905005964 BSEM-1101 Semester 3 
- **Module:** PROG211 Object-Oriented Programming 1, 
- **Lecturer:** Amadu Kamara

## The real-world problem

Clinics often track child and adult immunisation on paper. Records get lost, missed
doses go unnoticed, and it is hard to see how many people are fully protected.
This tool lets a health worker:

- register a patient under an **anonymous ID** (P001, P002, ...),
- record each vaccine dose (completed, scheduled or missed),
- update a record when its status changes,
- see one patient or all patients,
- see a **coverage summary** (how many patients are fully vaccinated per vaccine).

## How to run

Requires Python 3.8 or newer. No extra packages are needed.

```bash
git clone <your-repository-url>
cd vaccination_tracker
python main.py        # interactive menu
python demo.py        # automatic demonstration
python -m unittest -v # run the tests
```

In the menu, choose option **7** to load anonymous demo data and try everything quickly.

## Project structure

| File | Purpose |
|---|---|
| `models.py` | The classes: `Vaccine`, `Vaccination`, `Patient`, plus fixed reference data (tuples) |
| `tracker.py` | Functions that manage the patient dictionary (add, display, record, summary) |
| `main.py` | Text menu for health workers |
| `demo.py` | Non-interactive demonstration of every feature |
| `test_tracker.py` | Automated tests |

## How the code meets the assignment tasks

**Task 1 - OOP basics.** Three classes, each with attributes and methods:

- `Vaccine` (code, disease, doses_required) with `display_info()`
- `Vaccination` (record_id, vaccine, dose_number, date_given, status) with `update_status()` and `display_info()`
- `Patient` (patient_id, age_group, vaccinations) with `add_vaccination()`, `update_record()`, `display_info()`

The objects interact: a `Patient` creates `Vaccination` objects, and each `Vaccination` holds a `Vaccine` object.

**Task 2 - Data structures.** The program uses **one** collection type, the **dictionary**:
`patients = {patient_id: Patient}`, with `add_patient()` and `display_patients()` in `tracker.py`.
(Each patient's records are also kept in a dictionary, `record_id: Vaccination`.)
**Tuples** hold fixed reference data that must never change: `VACCINE_CATALOGUE`, `AGE_GROUPS` and `STATUSES`.

**Task 3 - Methods.**

| Type | Where | What it does |
|---|---|---|
| Instance method | `Patient.add_vaccination()`, `Patient.update_record()`, `Vaccination.update_status()` | Work on one specific object |
| Class method (`@classmethod`) | `Vaccine.from_code()`, `Patient.total_patients()` | Build a vaccine from the catalogue; count patients |
| Static method (`@staticmethod`) | `Patient.is_valid_id()`, `Vaccination.parse_date()` | Validation that needs no object |

## How this solution meets Digital Public Goods (DPG) standards

| DPG principle | How it is met |
|---|---|
| **Open-source** | The full source code is public on GitHub under the MIT licence (see `LICENSE`). Anyone can use, study, change and share it. |
| **Inclusive and accessible design** | Plain-language menus and prompts, numbered choices, no jargon, and clear error messages that say how to fix the problem (for example "Date must be in YYYY-MM-DD format, e.g. 2026-03-15"). It runs in a basic text terminal on low-cost computers and needs no internet. |
| **Privacy-respecting** | **No names, addresses, phone numbers, or national IDs are stored.** A patient is only a system-generated anonymous ID plus a broad age group (for example "2-5"). The ID validator rejects anything that is not in the form `P001`, so personal names cannot be entered as IDs. Data lives in memory only and is not written to disk or sent anywhere. |
| **Modular and reusable** | Separate files for classes, logic and menu. Small single-purpose functions. Vaccines, age groups and statuses are defined once in `models.py`, so a country can adapt the vaccine schedule by editing one tuple, with no change to the logic. Classes can be reused in other health projects. |

## Example usage (sample input and output)

Output of `python demo.py`:

```text
=== 1. Object creation and interaction ===
Created patients: P001, P002
Vaccine from class method: OPV - Polio (4 dose(s))
Linked record: P001-V01: OPV dose 1/4 | 2026-01-10 | Completed

=== 2. Dictionary: add and display records ===
Patient P001 | Age group: 0-1
  P001-V01: OPV dose 1/4 | 2026-01-10 | Completed
  P001-V02: BCG dose 1/1 | 2026-01-10 | Completed
--------------------------------------------------
Patient P002 | Age group: 2-5
  P002-V01: MEASLES dose 1/2 | 2025-11-05 | Completed
  P002-V02: MEASLES dose 2/2 | 2099-01-01 | Scheduled
--------------------------------------------------
Total patients: 2

=== 3. Instance, class and static methods ===
After update_record: P002-V02: MEASLES dose 2/2 | 2099-01-01 | Missed
Patient.total_patients() -> 2
Patient.is_valid_id('P001') -> True
Patient.is_valid_id('John Smith') -> False
Vaccination.parse_date('2026-13-45') -> None

=== 4. Friendly error handling ===
Problem: Patient 'P009' was not found.
Problem: Unknown vaccine code. Choose one of: BCG, OPV, PENTA, MEASLES, COVID19
Problem: BCG only needs 1 dose(s); all are already recorded.

=== 5. Coverage summary ===
Coverage summary (2 patient(s))
  BCG      1/2 fully vaccinated (50%)
  OPV      0/2 fully vaccinated (0%)
  PENTA    0/2 fully vaccinated (0%)
  MEASLES  0/2 fully vaccinated (0%)
  COVID19  0/2 fully vaccinated (0%)
```

Sample interactive session (menu option 1, then 3 = age group "6-12" is chosen
from the numbered list, then option 2 to record a vaccine):

```text
Choose an option (0-8): 1
Choose age group:  1) 0-1  2) 2-5  3) 6-12  4) 13-17  5) 18-59  6) 60+
Enter number: 3
Registered. Patient ID: P001
Choose an option (0-8): 2
Patient ID (e.g. P001): P001
Vaccine code: BCG
Date given (YYYY-MM-DD): 2026-01-10
Status (Completed/Scheduled/Missed):
Saved record P001-V01.
```

## Licence

MIT Licence. See `LICENSE`.
