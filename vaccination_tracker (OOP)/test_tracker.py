"""Basic tests. Run with:  python -m unittest -v"""

import unittest

import tracker
from models import Patient, Vaccination, Vaccine


class TestVaccinationTracker(unittest.TestCase):
    def setUp(self):
        self.patients = {}
        self.p = tracker.add_patient(self.patients, "0-1")

    def test_static_id_validation(self):
        self.assertTrue(Patient.is_valid_id("P001"))
        self.assertFalse(Patient.is_valid_id("John Smith"))

    def test_class_method_from_code(self):
        self.assertEqual(Vaccine.from_code("bcg").code, "BCG")
        self.assertIsNone(Vaccine.from_code("nope"))

    def test_add_and_link_record(self):
        rec = tracker.record_vaccination(self.patients, "P001", "OPV", "2026-01-10")
        self.assertEqual(rec.dose_number, 1)
        self.assertIs(self.p.vaccinations[rec.record_id], rec)

    def test_dose_limit(self):
        tracker.record_vaccination(self.patients, "P001", "BCG", "2026-01-10")
        with self.assertRaises(ValueError):
            tracker.record_vaccination(self.patients, "P001", "BCG", "2026-02-10")

    def test_update_record_and_full_vaccination(self):
        rec = tracker.record_vaccination(self.patients, "P001", "BCG", "2099-01-01", "Scheduled")
        self.assertFalse(self.p.is_fully_vaccinated(Vaccine.from_code("BCG")))
        self.p.update_record(rec.record_id, "Completed")
        self.assertTrue(self.p.is_fully_vaccinated(Vaccine.from_code("BCG")))

    def test_bad_inputs(self):
        with self.assertRaises(ValueError):
            tracker.record_vaccination(self.patients, "P001", "BCG", "15/01/2026")
        with self.assertRaises(KeyError):
            tracker.record_vaccination(self.patients, "P999", "BCG", "2026-01-10")
        self.assertIsNone(Vaccination.parse_date("2026-13-45"))


if __name__ == "__main__":
    unittest.main()
