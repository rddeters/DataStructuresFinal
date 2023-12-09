import unittest
from datetime import datetime
from Patient import Patient
from InsuranceInformation import InsuranceInformation


class TestPatient(unittest.TestCase):
    def test_validate_first_name(self):
        # Test validating a valid first name
        expected_test_name = "John"
        actual_test_name = Patient.validate_name("John", "First Name")
        self.assertEqual(expected_test_name, actual_test_name)

        # Test validating an empty first name, should raise a ValueError
        with self.assertRaises(ValueError):
            Patient.validate_name("", "First Name")

    def test_validate_last_name(self):
        # Test validating a valid last name
        expected_test_name = "Smith"
        actual_test_name = Patient.validate_name("Smith", "Last Name")
        self.assertEqual(expected_test_name, actual_test_name)

        # Test validating an empty last name, should raise a ValueError
        with self.assertRaises(ValueError):
            Patient.validate_name("", "Last Name")

    def test_validate_dob(self):
        # Test validating a valid date of birth
        expected_test_dob = "01-01-1990"
        actual_test_dob = Patient.validate_dob("01-01-1990", "Date of Birth")
        self.assertEqual(expected_test_dob, actual_test_dob)

        # Test validating an invalid date format, should raise a ValueError
        with self.assertRaises(ValueError):
            Patient.validate_dob("01011990", "Date of Birth")

    def test_validate_phone(self):
        # Test validating a valid phone number
        expected_test_phone = "515-515-5115"
        actual_test_phone = Patient.validate_phone("515-515-5115")
        self.assertEqual(expected_test_phone, actual_test_phone)

        # Test validating an invalid phone number format, should raise a ValueError
        with self.assertRaises(ValueError):
            Patient.validate_phone("5155155115")

    def test_validate_address(self):
        # Test validating a valid address
        expected_test_address = "111 1st St"
        actual_test_address = Patient.validate_address("111 1st St")
        self.assertEqual(expected_test_address, actual_test_address)

        # Test validating an empty address, should raise a ValueError
        with self.assertRaises(ValueError):
            Patient.validate_address("")

    def test_validate_last_exam(self):
        # Test validating a valid last exam date
        date_str = "01-01-2023"
        expected_test_exam = datetime.strptime(date_str, "%m-%d-%Y").date()
        actual_test_exam = Patient.validate_date(date_str, "Last Exam")
        self.assertEqual(expected_test_exam, actual_test_exam)

        # Test validating "N/A" as a valid last exam date
        none_date_str = "N/A"
        none_expected_exam = None
        none_actual_exam = Patient.validate_date(none_date_str, "Last Exam")
        self.assertEqual(none_expected_exam, none_actual_exam)

    def test_validate_prescription(self):
        # Test validating a valid prescription
        expected_test_script = "-0.75/DS/0, -0.25/DS/0"
        actual_test_script = Patient.validate_address("-0.75/DS/0, -0.25/DS/0")
        self.assertEqual(expected_test_script, actual_test_script)

        # Test validating "N/A" as a valid prescription
        none_script_str = "N/A"
        none_expected_script = None
        none_actual_script = Patient.validate_prescription(none_script_str)
        self.assertEqual(none_expected_script, none_actual_script)

        # Test validating an invalid prescription format, should raise a ValueError
        with self.assertRaises(ValueError):
            Patient.validate_prescription("*****")

        # Test validating an empty prescription, should raise a ValueError
        with self.assertRaises(ValueError):
            Patient.validate_prescription("")

    def test_validate_provider(self):
        # Test validating a valid insurance provider name
        expected_test_provider = "Blue Cross Blue Shield"
        actual_test_provider = InsuranceInformation.validate_optional_string("Blue Cross Blue Shield", "Provider Name")
        self.assertEqual(expected_test_provider, actual_test_provider)

        # Test validating "N/A" as a valid provider name
        none_provider_str = "N/A"
        none_expected_provider = None
        none_actual_provider = InsuranceInformation.validate_optional_string(none_provider_str, "Provider Name")
        self.assertEqual(none_expected_provider, none_actual_provider)

        # Test validating an invalid provider name format, should raise a ValueError
        with self.assertRaises(ValueError):
            InsuranceInformation.validate_optional_string("*****", "Provider Name")

        # Test validating an empty provider name, should raise a ValueError
        with self.assertRaises(ValueError):
            InsuranceInformation.validate_optional_string("", "Provider Name")

    def test_validate_policy_num(self):
        # Test validating a valid insurance policy number
        expected_test_policy = "XQW01234567"
        actual_test_policy = InsuranceInformation.validate_optional_string("XQW01234567", "Policy Number")
        self.assertEqual(expected_test_policy, actual_test_policy)

        # Test validating "N/A" as a valid policy number
        none_policy_str = "N/A"
        none_expected_policy = None
        none_actual_policy = InsuranceInformation.validate_optional_string(none_policy_str, "Policy Number")
        self.assertEqual(none_expected_policy, none_actual_policy)

        # Test validating an invalid policy number format, should raise a ValueError
        with self.assertRaises(ValueError):
            InsuranceInformation.validate_optional_string("*****", "Policy Number")

        # Test validating an empty policy number, should raise a ValueError
        with self.assertRaises(ValueError):
            InsuranceInformation.validate_optional_string("", "Policy Number")

    def test_validate_copay(self):
        # Test validating a valid copay value
        copay_str = "10"
        expected_test_copay = 10
        actual_test_copay = InsuranceInformation.validate_optional_int(copay_str)
        self.assertEqual(expected_test_copay, actual_test_copay)

        # Test validating "N/A" as a valid copay value
        none_copay_str = "N/A"
        none_expected_copay = None
        none_actual_copay = InsuranceInformation.validate_optional_int(none_copay_str)
        self.assertEqual(none_expected_copay, none_actual_copay)

        # Test validating an invalid copay value format, should raise a ValueError
        with self.assertRaises(ValueError):
            InsuranceInformation.validate_optional_int("Ten")

        # Test validating an empty copay value, should raise a ValueError
        with self.assertRaises(ValueError):
            InsuranceInformation.validate_optional_int("")


if __name__ == '__main__':
    unittest.main()
