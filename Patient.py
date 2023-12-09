from datetime import datetime, timedelta
import re


class Patient:
    def __init__(self, first_name, last_name, dob, phone, address, last_exam=None, emergent_issue=None,
                 prescription=None, conditions=None, primary_member=None, insurance_info=None):
        # Constructor initializes patient data
        self.first_name = self.validate_name(first_name, "First Name")
        self.last_name = self.validate_name(last_name, "Last Name")
        self.dob = self.validate_dob(dob, "Date of Birth")
        self.phone = self.validate_phone(phone)
        self.address = self.validate_address(address)
        self.last_exam = self.validate_date(last_exam, "Last Exam")
        self.prescription = self.validate_prescription(prescription)
        self.emergent_issue = emergent_issue
        self.prescription = prescription
        self.conditions = conditions
        self.primary_member = primary_member
        self.insurance_info = insurance_info
        self.next = None
        self.priority_level = self.calculate_priority()

    @staticmethod
    def validate_name(name, field_name):
        # Static method to validate and clean a name field
        if not name.strip():
            raise ValueError(f"{field_name} must be a non-empty string.")
        if not all(char.isalpha() or char in " '-" for char in name):
            raise ValueError(f"{field_name} contains invalid characters.")
        return name

    @staticmethod
    def validate_date(date_str, field_name):
        # Static method to validate and parse a date field
        if not date_str or date_str.strip().upper() == "N/A":
            return None
        try:
            return datetime.strptime(date_str, "%m-%d-%Y").date()
        except ValueError:
            raise ValueError(f"{field_name} must be a valid date string (MM-DD-YYYY) or 'N/A'.")

    @staticmethod
    def validate_phone(phone):
        # Static method to validate and clean a phone number
        phone_pattern = re.compile(r"^\d{3}-\d{3}-\d{4}$")
        if not phone_pattern.match(phone):
            raise ValueError("Phone number must be in the format 555-555-5555.")
        return phone

    @staticmethod
    def validate_dob(date_str, field_name):
        # Static method to validate and clean a date of birth field
        try:
            datetime.strptime(date_str, "%m-%d-%Y").date()
            return date_str
        except ValueError:
            raise ValueError(f"{field_name} must be a valid date string (MM-DD-YYYY) or 'N/A'.")

    @staticmethod
    def validate_address(address):
        # Static method to validate and clean an address field
        if not address.strip():
            raise ValueError("Address must be a non-empty string.")
        return address

    @staticmethod
    def validate_prescription(value):
        # Static method to validate and clean a prescription field
        if value == "N/A":
            return None
        if not value.strip():  # Check for an empty string
            raise ValueError("Prescription must be entered or 'N/A'.")
        if not all(char.isalnum() or char in " '-/" for char in value):
            raise ValueError("Prescription contains invalid characters.")
        else:
            return value

    def get_insurance_info(self):
        # Method to retrieve insurance information associated with the patient
        if self.insurance_info:
            return self.insurance_info
        elif self.primary_member:
            return self.primary_member.get_insurance_info()
        else:
            return None

    def calculate_priority(self):
        current_date = datetime.now().date()
        one_year_ago = current_date - timedelta(days=365)

        # Convert last_exam from string to datetime object
        if isinstance(self.last_exam, str):
            try:
                last_exam_date = datetime.strptime(self.last_exam, "%m-%d-%Y").date()
            except ValueError:
                # Handle invalid date format
                last_exam_date = None
        elif isinstance(self.last_exam, datetime):
            last_exam_date = self.last_exam.date()
        else:
            last_exam_date = None

        if self.emergent_issue:
            return 1  # Priority 1 for emergent issues
        elif self.conditions and (last_exam_date is None or last_exam_date <= one_year_ago):
            if last_exam_date is None:
                self.last_exam = "N/A"
            return 2  # Priority 2 for medical conditions with last exam over a year ago or no last exam
        elif not self.conditions and (last_exam_date is None or last_exam_date <= one_year_ago):
            if last_exam_date is None:
                self.last_exam = "N/A"
            return 3  # Priority 3 for no conditions with last exam over a year ago or no last exam
        else:
            return 4  # Priority 4 for all others


class PatientLinkedList:
    def __init__(self):
        self.head = None

    def insert_patient(self, new_patient):
        # Method to insert a new patient into the linked list
        if not self.head:
            self.head = new_patient
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_patient

    def find_patient(self, first_name, last_name):
        # Method to find a patient by first and last name
        current = self.head
        while current:
            if current.first_name == first_name and current.last_name == last_name:
                return current
            current = current.next
        return None

    def delete_patient(self, first_name, last_name):
        # Method to delete a patient by first and last name
        current = self.head
        previous = None
        while current:
            if current.first_name == first_name and current.last_name == last_name:
                if previous:
                    previous.next = current.next
                else:
                    self.head = current.next
                return True
            previous = current
            current = current.next
        return False

    def edit_patient(self, first_name, last_name, **updates):
        # Method to edit patient information by first and last name
        patient = self.find_patient(first_name, last_name)
        if patient:
            for attribute, new_value in updates.items():
                setattr(patient, attribute, new_value)
            return True
        return False

    def print_list(self):
        # Method to print the list of patients with their information
        current = self.head
        while current:
            print(
                f"Patient: {current.first_name} {current.last_name}, Last Exam: {current.last_exam}, "
                f"Emergent Issue: {current.emergent_issue}, Conditions: {current.conditions}, "
                f"Priority: {current.priority_level}")
            current = current.next
