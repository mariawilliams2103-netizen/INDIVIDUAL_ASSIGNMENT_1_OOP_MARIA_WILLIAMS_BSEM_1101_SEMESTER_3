"""Domain classes for the Vaccination Tracker.

Privacy note (DPG): no names, addresses, phone numbers or national IDs are
stored. A patient is only an anonymous system-generated ID plus an age group.

Data-structure note (Task 2): the program uses ONE collection type, the
dictionary. Tuples are used only for fixed, read-only reference data.
"""

import re
from datetime import date, datetime

# ---------------------------------------------------------------------------
# Fixed reference data (tuples: immutable, so they cannot be changed by accident)
# Each vaccine entry is (code, disease protected against, doses required).
# ---------------------------------------------------------------------------
VACCINE_CATALOGUE = (
    ("BCG", "Tuberculosis", 1),
    ("OPV", "Polio", 4),
    ("PENTA", "Diphtheria, Tetanus, Pertussis, Hepatitis B, Hib", 3),
    ("MEASLES", "Measles", 2),
    ("COVID19", "COVID-19", 2),
)

AGE_GROUPS = ("0-1", "2-5", "6-12", "13-17", "18-59", "60+")

STATUSES = ("Completed", "Scheduled", "Missed")

DATE_FORMAT = "%Y-%m-%d"


class Vaccine:
    """A type of vaccine (reference information, not tied to any person)."""

    def __init__(self, code, disease, doses_required):
        self.code = code
        self.disease = disease
        self.doses_required = doses_required

    @classmethod
    def from_code(cls, code):
        """Class method: build a Vaccine from the catalogue using its code.

        Returns None if the code is not in the catalogue.
        """
        wanted = str(code).strip().upper()
        for cat_code, disease, doses in VACCINE_CATALOGUE:
            if cat_code == wanted:
                return cls(cat_code, disease, doses)
        return None

    def display_info(self):
        return f"{self.code} - {self.disease} ({self.doses_required} dose(s))"


class Vaccination:
    """One vaccination event (a dose) that belongs to a patient."""

    def __init__(self, record_id, vaccine, dose_number, date_given, status="Completed"):
        self.record_id = record_id
        self.vaccine = vaccine          # a Vaccine object (object interaction)
        self.dose_number = dose_number
        self.date_given = date_given    # string in YYYY-MM-DD form
        self.status = status

    @staticmethod
    def parse_date(text):
        """Static method: turn 'YYYY-MM-DD' into a date, or None if invalid."""
        try:
            return datetime.strptime(str(text).strip(), DATE_FORMAT).date()
        except ValueError:
            return None

    def update_status(self, new_status):
        """Instance method: change the status of this vaccination record."""
        if new_status not in STATUSES:
            raise ValueError(f"Status must be one of: {', '.join(STATUSES)}")
        self.status = new_status

    def display_info(self):
        return (f"  {self.record_id}: {self.vaccine.code} dose "
                f"{self.dose_number}/{self.vaccine.doses_required} | "
                f"{self.date_given} | {self.status}")


class Patient:
    """An anonymous patient. Holds their vaccination records."""

    _total_patients = 0   # class attribute shared by every Patient

    ID_PATTERN = re.compile(r"^P\d{3,}$")

    def __init__(self, patient_id, age_group):
        if not Patient.is_valid_id(patient_id):
            raise ValueError("Patient ID must look like P001 (letter P + digits).")
        if age_group not in AGE_GROUPS:
            raise ValueError(f"Age group must be one of: {', '.join(AGE_GROUPS)}")
        self.patient_id = patient_id
        self.age_group = age_group
        self.vaccinations = {}   # record_id -> Vaccination (dictionary)
        Patient._total_patients += 1

    # -- class and static methods -------------------------------------------
    @classmethod
    def total_patients(cls):
        """Class method: how many Patient objects have been created."""
        return cls._total_patients

    @staticmethod
    def is_valid_id(patient_id):
        """Static method: check the anonymous ID format (e.g. P001)."""
        return bool(Patient.ID_PATTERN.match(str(patient_id)))

    # -- instance methods ---------------------------------------------------
    def doses_recorded(self, vaccine_code, completed_only=False):
        """Count this patient's records for one vaccine."""
        return sum(
            1 for v in self.vaccinations.values()
            if v.vaccine.code == vaccine_code
            and (not completed_only or v.status == "Completed")
        )

    def add_vaccination(self, vaccine, date_given, status="Completed"):
        """Record a new dose for this patient and return the new record.

        Raises ValueError with a plain-language message if something is wrong.
        """
        parsed = Vaccination.parse_date(date_given)
        if parsed is None:
            raise ValueError("Date must be in YYYY-MM-DD format, e.g. 2026-03-15.")
        if status not in STATUSES:
            raise ValueError(f"Status must be one of: {', '.join(STATUSES)}")
        if status == "Completed" and parsed > date.today():
            raise ValueError("A completed dose cannot have a future date. "
                             "Use status 'Scheduled' instead.")
        dose_number = self.doses_recorded(vaccine.code) + 1
        if dose_number > vaccine.doses_required:
            raise ValueError(f"{vaccine.code} only needs {vaccine.doses_required} "
                             "dose(s); all are already recorded.")
        record_id = f"{self.patient_id}-V{len(self.vaccinations) + 1:02d}"
        record = Vaccination(record_id, vaccine, dose_number, date_given.strip(), status)
        self.vaccinations[record_id] = record
        return record

    def update_record(self, record_id, new_status):
        """Change the status of one of this patient's vaccination records."""
        record = self.vaccinations.get(record_id)
        if record is None:
            raise KeyError(f"No record '{record_id}' for patient {self.patient_id}.")
        record.update_status(new_status)
        return record

    def is_fully_vaccinated(self, vaccine):
        """True if all required doses of this vaccine are marked Completed."""
        return self.doses_recorded(vaccine.code, completed_only=True) >= vaccine.doses_required

    def display_info(self):
        lines = f"Patient {self.patient_id} | Age group: {self.age_group}"
        if not self.vaccinations:
            return lines + "\n  (no vaccination records yet)"
        for record in self.vaccinations.values():
            lines += "\n" + record.display_info()
        return lines
