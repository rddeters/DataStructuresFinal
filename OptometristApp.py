import tkinter as tk
from datetime import datetime, timedelta
from tkinter import messagebox
from Patient import Patient, PatientLinkedList
from InsuranceInformation import InsuranceInformation
from InsuranceFamilyTree import InsuranceFamilyTree, FamilyTreeNode
from AppointmentScheduler import AppointmentScheduler


class OptometristApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        # Initialize the main application window
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("700x650")  # Set the window size

        # Initialize shared resources
        self.patient_list = PatientLinkedList()
        self.family_tree = InsuranceFamilyTree()

        # Create a container for all frames
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        container.configure(background='#DCDCDD')

        self.frames = {}

        # Create instances of different frames and store them in a dictionary
        for F in (HomePage, AddNewFamilyPage, SearchPatientPage, SearchFamilyPage, EditPatientPage, AddPatientPage,
                  ScheduleAppointmentPage, ViewAllPatientsPage):
            frame = F(container, controller=self, linked_list=self.patient_list, family_tree=self.family_tree)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Show the initial frame (HomePage)
        self.show_frame(HomePage)

    def show_frame(self, cont):
        # Show the specified frame and perform additional actions if needed
        frame = self.frames[cont]
        if cont == ScheduleAppointmentPage:
            frame.refresh_page()
        if cont == ViewAllPatientsPage:
            frame.refresh_page()
        frame.tkraise()


class HomePage(tk.Frame):
    def __init__(self, parent, controller, linked_list, family_tree):
        # Initialize the home page frame
        tk.Frame.__init__(self, parent, background='#DCDCDD')  # Set background color
        self.controller = controller
        self.linked_list = linked_list
        self.family_tree = family_tree

        # Style configuration
        title_font = ("Helvetica", 16, "bold")
        subtitle_font = ("Helvetica", 14)
        button_font = ("Helvetica", 12)
        button_color = "#C5C3C6"

        # Title Label
        label = tk.Label(self, text="Optometrist Portal", font=title_font, bg='#DCDCDD')
        label.pack(pady=10)

        # Subtitle
        subtitle = tk.Label(self, text="Home Page", font=subtitle_font, bg='#DCDCDD')
        subtitle.pack(pady=5)

        # Buttons for various actions
        add_new_family_button = tk.Button(self, text="Add New Family", font=button_font, bg=button_color,
                                          command=lambda: controller.show_frame(AddNewFamilyPage))
        add_new_family_button.pack(padx=5, pady=5)

        search_button = tk.Button(self, text="Search by Patient", font=button_font, bg=button_color,
                                  command=lambda: controller.show_frame(SearchPatientPage))
        search_button.pack(padx=5, pady=5)

        search_button = tk.Button(self, text="Search Family by Primary Member", font=button_font, bg=button_color,
                                  command=lambda: controller.show_frame(SearchFamilyPage))
        search_button.pack(padx=5, pady=5)

        schedule_button = tk.Button(self, text="List of Patients to Schedule", font=button_font, bg=button_color,
                                    command=lambda: controller.show_frame(ScheduleAppointmentPage))
        schedule_button.pack(padx=5, pady=5)

        view_all_patients_button = tk.Button(self, text="List of All Patients", font=button_font, bg=button_color,
                                             command=lambda: controller.show_frame(ViewAllPatientsPage))
        view_all_patients_button.pack(padx=5, pady=5)


class SearchFamilyPage(tk.Frame):
    def __init__(self, parent, controller, linked_list, family_tree):
        # Initialize the SearchFamilyPage frame
        tk.Frame.__init__(self, parent, background='#DCDCDD')  # Set background color
        self.controller = controller
        self.linked_list = linked_list
        self.family_tree = family_tree
        self.family_info_widgets = []  # Store widgets for family information display

        # Style configuration
        label_font = ("Helvetica", 12)
        entry_font = ("Helvetica", 10)
        button_font = ("Helvetica", 10)
        button_color = "#C5C3C6"

        # Title and Subtitle
        title = tk.Label(self, text="Search Primary Family Member", font=("Helvetica", 16), bg='#DCDCDD')
        title.pack(pady=10)
        subtitle = tk.Label(self, text="Please enter details", font=("Helvetica", 14), bg='#DCDCDD')
        subtitle.pack()

        # Entry Frame
        entry_frame = tk.Frame(self, bg='#DCDCDD')
        entry_frame.pack(pady=10)

        # First Name Entry
        first_name_label = tk.Label(entry_frame, text="First Name:", font=label_font, bg='#DCDCDD')
        first_name_label.grid(row=0, column=0, padx=5, pady=5)
        self.first_name_entry = tk.Entry(entry_frame, font=entry_font)
        self.first_name_entry.grid(row=0, column=1, padx=5, pady=5)

        # Last Name Entry
        last_name_label = tk.Label(entry_frame, text="Last Name:", font=label_font, bg='#DCDCDD')
        last_name_label.grid(row=1, column=0, padx=5, pady=5)
        self.last_name_entry = tk.Entry(entry_frame, font=entry_font)
        self.last_name_entry.grid(row=1, column=1, padx=5, pady=5)

        # Date of Birth Entry
        dob_label = tk.Label(entry_frame, text="Date of Birth:", font=label_font, bg='#DCDCDD')
        dob_label.grid(row=2, column=0, padx=5, pady=5)
        self.dob_entry = tk.Entry(entry_frame, font=entry_font)
        self.dob_entry.grid(row=2, column=1, padx=5, pady=5)

        # Button Frame
        button_frame = tk.Frame(self, bg='#DCDCDD')
        button_frame.pack(pady=5)

        # Search and Home buttons
        reset_button = tk.Button(button_frame, text="Search", font=button_font, bg=button_color,
                                 command=self.search_patient)
        reset_button.pack(side="left", padx=5)

        home_button = tk.Button(button_frame, text="Home", font=button_font, bg=button_color, command=self.go_home)
        home_button.pack(side="left", padx=5)

        # Frame for Family Info Display
        self.family_info_frame = tk.Frame(self, bg='#DCDCDD')
        self.family_info_frame.pack(pady=10)

    def go_home(self):
        # Reset the page and go to the HomePage
        self.reset_page()
        self.controller.show_frame(HomePage)

    def is_patient_match(self, patient, first_name, last_name, dob):
        return (patient and
                patient.first_name == first_name and
                patient.last_name == last_name and
                patient.dob == dob)

    def search_patient(self):
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        dob = self.dob_entry.get()  # Assuming you have an entry field for dob

        # Search for the family member
        found_tree = self.search_family_member(first_name, last_name, dob)
        if found_tree:
            self.display_family_info(found_tree)
        else:
            messagebox.showinfo("Search Result", "No patients found with the provided information.")

    def search_family_member(self, first_name, last_name, dob):
        for family in self.family_tree.root.children:
            if self.is_patient_match(family.patient, first_name, last_name, dob):
                return family

            for child in family.children:
                if self.is_patient_match(child.patient, first_name, last_name, dob):
                    return child
        return None

    def reset_page(self):
        # Reset input fields
        self.first_name_entry.delete(0, tk.END)
        self.last_name_entry.delete(0, tk.END)
        self.dob_entry.delete(0, tk.END)

        # Clear displayed family information
        for widget in self.family_info_frame.winfo_children():
            widget.destroy()

        # Reset the current family tree node
        self.current_family_tree = None

    def display_family_info(self, family_tree):
        # Clear previous search results
        self.reset_page()

        # Styling configuration
        button_font = ("Helvetica", 12)
        button_color = "#C5C3C6"

        # Display primary family member info and buttons
        self.display_patient_info(family_tree.patient, is_primary=True)

        # Display children info and buttons
        for child in family_tree.children:
            self.display_patient_info(child.patient)

        # Store the current family tree node
        self.current_family_tree = family_tree

        # Add Patient Button
        add_patient_button = tk.Button(self.family_info_frame, text="Add Patient", font=button_font, bg=button_color,
                                       command=self.add_patient)
        add_patient_button.pack(pady=(15, 5))

    def display_patient_info(self, patient, is_primary=False):
        # Patient info label
        patient_info = f"{'Primary Member' if is_primary else 'Child'}: {patient.first_name} {patient.last_name}"
        patient_label = tk.Label(self.family_info_frame, text=patient_info, font=("Helvetica", 12), bg='#DCDCDD')
        patient_label.pack(pady=(5, 0))

        # Button configuration
        button_font = ("Helvetica", 12)
        button_color = "#C5C3C6"

        # View, Edit, and Delete buttons for the patient
        view_info_button = tk.Button(self.family_info_frame, text="View Patient Information", font=button_font,
                                     bg=button_color, command=lambda: self.view_patient_info(patient))
        view_info_button.pack(pady=(5, 0))

        edit_button = tk.Button(self.family_info_frame, text="Edit Patient", font=button_font, bg=button_color,
                                command=lambda: self.edit_patient(patient))
        edit_button.pack(pady=(5, 0))

        delete_button = tk.Button(self.family_info_frame, text="Delete Patient", font=button_font, bg=button_color,
                                  command=lambda: self.delete_patient(patient))
        delete_button.pack(pady=(5, 10))

    def delete_patient(self, patient):
        response = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this patient?")
        if response:
            self.perform_deletion(patient)

    def perform_deletion(self, patient):
        # Check if the patient is a primary member
        for family in self.family_tree.root.children:
            if family.patient == patient:
                # Delete all children of the primary member first
                while family.children:
                    child_patient = family.children[0].patient
                    self.linked_list.delete_patient(child_patient.first_name, child_patient.last_name)
                    family.children.pop(0)  # Remove the child from the tree
                # Remove the primary member from the tree
                self.family_tree.root.children.remove(family)
                break
            else:
                # Check if the patient is a child in any family
                for child in family.children:
                    if child.patient == patient:
                        family.children.remove(child)
                        break

        # Delete patient from linked list
        self.linked_list.delete_patient(patient.first_name, patient.last_name)

        self.refresh_family_display()

    def view_patient_info(self, patient):
        # Create a new top-level window to display patient info
        info_window = tk.Toplevel(self, background='#DCDCDD')
        info_window.title(f"Information for {patient.first_name} {patient.last_name}")

        label_font = ("Helvetica", 10)
        info_font = ("Helvetica", 10)
        button_font = ("Helvetica", 10)
        button_color = "#C5C3C6"

        # Function to create labels in a consistent style
        def create_label(text, font=label_font, container=info_window):
            tk.Label(container, text=text, font=font, bg='#DCDCDD').pack(pady=(5, 0))

        # Display patient info on separate labels
        create_label(f"First Name: {patient.first_name}", info_font)
        create_label(f"Last Name: {patient.last_name}", info_font)
        create_label(f"DOB: {patient.dob}", info_font)
        create_label(f"Phone: {patient.phone}", info_font)
        create_label(f"Address: {patient.address}", info_font)
        create_label(f"Last Exam: {patient.last_exam}", info_font)
        create_label(f"Emergent Issue: {'Yes' if patient.emergent_issue else 'No'}", info_font)
        create_label(f"Prescription: {patient.prescription}", info_font)
        create_label(f"Medical Conditions: {'Yes' if patient.conditions else 'No'}", info_font)

        # Insurance information
        if patient.insurance_info:
            create_label("Insurance Information:", info_font)
            create_label(f"Primary Member: {patient.insurance_info.primary_name}", info_font)
            create_label(f"Provider: {patient.insurance_info.provider_name}", info_font)
            create_label(f"Policy Number: {patient.insurance_info.policy_number}", info_font)
            create_label(f"Vision Coverage: {'Yes' if patient.insurance_info.vision_coverage else 'No'}", info_font)
            create_label(f"Medical Coverage: {'Yes' if patient.insurance_info.medical_coverage else 'No'}", info_font)
            create_label(f"Copay: {patient.insurance_info.copay}", info_font)
        else:
            create_label("No Insurance Information Available", info_font)

        # Close button
        close_button = tk.Button(info_window, text="Close", font=button_font, bg=button_color,
                                 command=info_window.destroy)
        close_button.pack(pady=10)

    def edit_patient(self, patient):
        edit_page = self.controller.frames[EditPatientPage]
        edit_page.load_patient(patient)
        self.controller.show_frame(EditPatientPage)
        self.reset_page()

    def add_patient(self):
        add_patient_page = self.controller.frames[AddPatientPage]
        add_patient_page.set_current_family_tree(self.current_family_tree)
        self.controller.show_frame(AddPatientPage)

    def refresh_family_display(self):
        if self.current_family_tree:
            self.display_family_info(self.current_family_tree)


class SearchPatientPage(tk.Frame):
    def __init__(self, parent, controller, linked_list, family_tree):
        # Initialize the SearchPatientPage frame
        tk.Frame.__init__(self, parent, background='#DCDCDD')  # Set background color
        self.controller = controller
        self.linked_list = linked_list
        self.family_tree = family_tree
        self.family_info_widgets = []  # Store widgets for family information display

        # Style configuration
        label_font = ("Helvetica", 12)
        entry_font = ("Helvetica", 10)
        button_font = ("Helvetica", 10)
        button_color = "#C5C3C6"

        # Title and Subtitle
        title = tk.Label(self, text="Search Patient", font=("Helvetica", 16), bg='#DCDCDD')
        title.pack(pady=10)
        subtitle = tk.Label(self, text="Please enter details", font=("Helvetica", 14), bg='#DCDCDD')
        subtitle.pack()

        # Entry Frame
        entry_frame = tk.Frame(self, bg='#DCDCDD')
        entry_frame.pack(pady=10)

        # First Name Entry
        first_name_label = tk.Label(entry_frame, text="First Name:", font=label_font, bg='#DCDCDD')
        first_name_label.grid(row=0, column=0, padx=5, pady=5)
        self.first_name_entry = tk.Entry(entry_frame, font=entry_font)
        self.first_name_entry.grid(row=0, column=1, padx=5, pady=5)

        # Last Name Entry
        last_name_label = tk.Label(entry_frame, text="Last Name:", font=label_font, bg='#DCDCDD')
        last_name_label.grid(row=1, column=0, padx=5, pady=5)
        self.last_name_entry = tk.Entry(entry_frame, font=entry_font)
        self.last_name_entry.grid(row=1, column=1, padx=5, pady=5)

        # Date of Birth Entry
        dob_label = tk.Label(entry_frame, text="Date of Birth:", font=label_font, bg='#DCDCDD')
        dob_label.grid(row=2, column=0, padx=5, pady=5)
        self.dob_entry = tk.Entry(entry_frame, font=entry_font)
        self.dob_entry.grid(row=2, column=1, padx=5, pady=5)

        # Button Frame
        button_frame = tk.Frame(self, bg='#DCDCDD')
        button_frame.pack(pady=5)

        # Search and Home buttons
        reset_button = tk.Button(button_frame, text="Search", font=button_font, bg=button_color,
                                 command=self.search_patient)
        reset_button.pack(side="left", padx=5)

        home_button = tk.Button(button_frame, text="Home", font=button_font, bg=button_color, command=self.go_home)
        home_button.pack(side="left", padx=5)

        # Frame for Patient Info Display
        self.patient_info_frame = tk.Frame(self, bg='#DCDCDD')
        self.patient_info_frame.pack(pady=10)

        self.insurance_frame = tk.Frame(self, bg='#DCDCDD')
        self.insurance_frame.pack(pady=10)

        self.patient_buttons_frame = tk.Frame(self, bg='#DCDCDD')
        self.patient_buttons_frame.pack(pady=10)

    def reset_page(self):
        # Reset input fields
        self.first_name_entry.delete(0, tk.END)
        self.last_name_entry.delete(0, tk.END)
        self.dob_entry.delete(0, tk.END)

        # Clear displayed patient information
        for widget in self.patient_info_frame.winfo_children():
            widget.destroy()
        for widget in self.insurance_frame.winfo_children():
            widget.destroy()
        for widget in self.patient_buttons_frame.winfo_children():
            widget.destroy()

    def go_home(self):
        # Reset the page and go to the HomePage
        self.reset_page()
        self.controller.show_frame(HomePage)

    def search_patient(self):
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        dob = self.dob_entry.get()
        patient = self.find_patient(first_name, last_name, dob)
        if patient:
            self.display_patient_info(patient)
        else:
            messagebox.showinfo("Search Result", "No patient found with the provided information.")

    def find_patient(self, first_name, last_name, dob):
        # Search for a patient in the linked list
        current = self.linked_list.head
        while current:
            if current.first_name == first_name and current.last_name == last_name and current.dob == dob:
                return current
            current = current.next
        return None

    def display_patient_info(self, patient):
        # Clear previous search results
        self.reset_page()

        info_font = ("Helvetica", 10)
        button_font = ("Helvetica", 10)
        button_color = "#C5C3C6"

        # Function to create labels in a grid
        def create_patient_label(row, column, text, font=info_font, container=self.patient_info_frame):
            tk.Label(container, text=text, font=font, bg='#DCDCDD').grid(row=row, column=column, sticky='w', padx=5,
                                                                         pady=2)

        def create_insurance_label(row, column, text, font=info_font, container=self.insurance_frame):
            tk.Label(container, text=text, font=font, bg='#DCDCDD').grid(row=row, column=column, sticky='w', padx=5,
                                                                         pady=2)

        # Display patient info in a grid layout
        labels = [
            f"First Name: {patient.first_name}", f"Last Name: {patient.last_name}",
            f"DOB: {patient.dob}", f"Phone: {patient.phone}",
            f"Address: {patient.address}", f"Last Exam: {patient.last_exam}",
            f"Emergent Issue: {'Yes' if patient.emergent_issue else 'No'}",
            f"Prescription: {patient.prescription if patient.prescription else 'None'}",
            f"Medical Conditions: {'Yes' if patient.conditions else 'No'}"
        ]

        if patient.insurance_info:
            ins_labels = [
                f"Primary Member: {patient.insurance_info.primary_name}",
                f"Provider: {patient.insurance_info.provider_name}",
                f"Policy Number: {patient.insurance_info.policy_number}",
                f"Vision Coverage: {'Yes' if patient.insurance_info.vision_coverage else 'No'}",
                f"Medical Coverage: {'Yes' if patient.insurance_info.medical_coverage else 'No'}",
                f"Copay: {patient.insurance_info.copay}"
            ]
        else:
            ins_labels = ["No Insurance Information Available"]

        for i, text in enumerate(labels):
            create_patient_label(i // 2, i % 2, text)

        for i, text in enumerate(ins_labels):
            create_insurance_label(i // 2, i % 2, text)

        # Edit Patient Button
        edit_button = tk.Button(self.patient_buttons_frame, text="Edit Patient", font=button_font, bg=button_color,
                                command=lambda: self.edit_patient(patient))
        edit_button.pack(pady=(5, 0))

    def edit_patient(self, patient):
        # Load the patient data into the EditPatientPage and switch to that page
        edit_page = self.controller.frames[EditPatientPage]
        edit_page.load_patient(patient)
        self.reset_page()
        self.controller.show_frame(EditPatientPage)


class EditPatientPage(tk.Frame):
    def __init__(self, parent, controller, linked_list, family_tree):
        # Initialize the EditPatientPage frame
        tk.Frame.__init__(self, parent, background='#DCDCDD')
        self.controller = controller
        self.linked_list = linked_list
        self.family_tree = family_tree
        self.current_patient = None

        label_font = ("Helvetica", 12)
        entry_font = ("Helvetica", 12)
        button_font = ("Helvetica", 12)
        button_color = "#C5C3C6"

        # Title and Subtitle
        title = tk.Label(self, text="Edit Patient", font=("Helvetica", 16), bg='#DCDCDD')
        title.pack(pady=10)
        subtitle = tk.Label(self, text="Please enter details", font=("Helvetica", 14), bg='#DCDCDD')
        subtitle.pack()

        # Create Entry Fields for Patient Data
        self.first_name_entry = self.create_label_entry("First Name", label_font, entry_font)
        self.last_name_entry = self.create_label_entry("Last Name", label_font, entry_font)
        self.dob_entry = self.create_label_entry("Date of Birth", label_font, entry_font)
        self.phone_number_entry = self.create_label_entry("Phone Number", label_font, entry_font)
        self.address_entry = self.create_label_entry("Address", label_font, entry_font)
        self.last_exam_entry = self.create_label_entry("Last Exam", label_font, entry_font)

        # Create Radio Buttons for Emergent Issue and Medical Conditions
        self.emergent_issue = tk.BooleanVar(value=False)
        self.create_radio_buttons("Emergent Issue", self.emergent_issue, label_font)
        self.prescription_entry = self.create_label_entry("Prescription", label_font, entry_font)
        self.conditions = tk.BooleanVar(value=False)
        self.create_radio_buttons("Medical Conditions", self.conditions, label_font)

        # Submit Button
        submit_button = tk.Button(self, text="Submit", font=button_font, bg=button_color,
                                  command=self.submit_changes)
        submit_button.pack(pady=5)

        # Reset Button
        reset_button = tk.Button(self, text="Reset", font=button_font, bg=button_color, command=self.reset_form)
        reset_button.pack(pady=5)

        # Home Button
        home_button = tk.Button(self, text="Home", font=button_font, bg=button_color,
                                command=lambda: controller.show_frame(HomePage))
        home_button.pack(pady=5)

    def create_radio_buttons(self, label_text, variable, label_font):
        # Create a set of radio buttons for a boolean variable
        frame = tk.Frame(self, bg='#DCDCDD')
        frame.pack(pady=5)

        label = tk.Label(frame, text=label_text, font=label_font, bg='#DCDCDD')
        label.pack(side="left")

        yes_button = tk.Radiobutton(frame, text="Yes", variable=variable, value=True, bg='#DCDCDD')
        yes_button.pack(side="left")

        no_button = tk.Radiobutton(frame, text="No", variable=variable, value=False, bg='#DCDCDD')
        no_button.pack(side="left")

        return variable

    def create_label_entry(self, label_text, label_font, entry_font):
        # Create a label-entry pair for patient data
        frame = tk.Frame(self, bg='#DCDCDD')
        frame.pack(pady=5)

        label = tk.Label(frame, text=label_text, font=label_font, bg='#DCDCDD')
        label.pack(side="left")

        entry = tk.Entry(frame, font=entry_font)
        entry.pack(side="right", expand=True, fill="x")

        return entry

    def load_patient(self, patient):
        # Load patient data into the form
        self.current_patient = patient
        self.first_name_entry.delete(0, tk.END)
        self.first_name_entry.insert(0, patient.first_name)
        self.last_name_entry.delete(0, tk.END)
        self.last_name_entry.insert(0, patient.last_name)

        # Handle 'dob' attribute
        dob_str = self.format_date(patient.dob)
        self.dob_entry.delete(0, tk.END)
        self.dob_entry.insert(0, dob_str)

        self.phone_number_entry.delete(0, tk.END)
        self.phone_number_entry.insert(0, patient.phone)
        self.address_entry.delete(0, tk.END)
        self.address_entry.insert(0, patient.address)

        # Handle 'last_exam' attribute
        last_exam_str = self.format_date(patient.last_exam)
        self.last_exam_entry.delete(0, tk.END)
        self.last_exam_entry.insert(0, last_exam_str)

        self.prescription_entry.delete(0, tk.END)
        self.prescription_entry.insert(0, patient.prescription)

    def format_date(self, date_value):
        # Format a date value as a string
        if isinstance(date_value, datetime):
            return date_value.strftime("%m-%d-%Y")
        elif date_value is None or date_value == 'None':
            return "None"
        else:
            return date_value  # assuming it's already a string in the correct format

    def submit_changes(self):
        # Update patient information and linked list
        try:
            self.current_patient.first_name = Patient.validate_name(self.first_name_entry.get(), "First Name")
            self.current_patient.last_name = Patient.validate_name(self.last_name_entry.get(), "Last Name")
            self.current_patient.dob = Patient.validate_date(self.dob_entry.get(), "Date of Birth")
            self.current_patient.phone = Patient.validate_phone(self.phone_number_entry.get())
            self.current_patient.address = Patient.validate_address(self.address_entry.get())
            self.current_patient.last_exam = Patient.validate_date(self.last_exam_entry.get(), "Last Exam")

            self.current_patient.emergent_issue = self.emergent_issue.get()
            self.current_patient.prescription = Patient.validate_prescription(self.prescription_entry.get())
            self.current_patient.priority_level = self.calculate_priority(self.current_patient.last_exam,
                                                                          self.current_patient.conditions,
                                                                          self.current_patient.emergent_issue)
            if self.current_patient.last_exam is None:
                self.current_patient.last_exam = "N/A"

            # Prepare the update data, excluding first_name and last_name
            update_data = self.get_patient_data()
            del update_data["first_name"]
            del update_data["last_name"]

            # Update patient in the linked list
            self.linked_list.edit_patient(first_name=self.current_patient.first_name,
                                          last_name=self.current_patient.last_name, **update_data)

            # Notify user
            messagebox.showinfo("Success", "Patient information updated.")

            # Refresh the SearchPage and navigate as needed
            search_page = self.controller.frames[SearchFamilyPage]
            search_page.refresh_family_display()
            self.controller.show_frame(HomePage)
        except ValueError as ve:
            messagebox.showerror("Input Error", str(ve))

    def calculate_priority(self, last_exam, conditions, emergent_issue):
        # Calculate the priority level based on patient data
        current_date = datetime.now().date()
        one_year_ago = current_date - timedelta(days=365)

        # Convert last_exam from string to datetime object
        if isinstance(last_exam, str):
            try:
                last_exam_date = datetime.strptime(last_exam, "%m-%d-%Y").date()
            except ValueError:
                # Handle invalid date format
                last_exam_date = None
        elif isinstance(last_exam, datetime):
            last_exam_date = last_exam.date()
        else:
            last_exam_date = None

        if emergent_issue:
            return 1  # Priority 1 for emergent issues
        elif conditions and (last_exam_date is None or last_exam_date <= one_year_ago):
            return 2  # Priority 2 for medical conditions with last exam over a year ago or no last exam
        elif not conditions and (last_exam_date is None or last_exam_date <= one_year_ago):
            return 3  # Priority 3 for no conditions with last exam over a year ago or no last exam
        else:
            return 4  # Priority 4 for all others

    def get_patient_data(self):
        # Collect data from all fields
        return {
            "first_name": self.first_name_entry.get(),
            "last_name": self.last_name_entry.get(),
            "dob": self.dob_entry.get(),
            "phone": self.phone_number_entry.get(),
            "address": self.address_entry.get(),
            "last_exam": self.last_exam_entry.get(),
            "prescription": self.prescription_entry.get()
        }

    def reset_form(self):
        # Reset form fields to the patient's original information
        if self.current_patient:
            self.load_patient(self.current_patient)


class AddPatientPage(tk.Frame):
    def __init__(self, parent, controller, linked_list, family_tree):
        # Initialize the AddPatientPage frame
        tk.Frame.__init__(self, parent, background='#DCDCDD')
        self.controller = controller
        self.linked_list = linked_list
        self.family_tree = family_tree
        self.current_family_tree = None

        label_font = ("Helvetica", 12)
        entry_font = ("Helvetica", 12)
        button_font = ("Helvetica", 12)
        button_color = "#C5C3C6"

        # Title and Subtitle
        title = tk.Label(self, text="Add Patient", font=("Helvetica", 16), bg='#DCDCDD')
        title.pack(pady=10)
        subtitle = tk.Label(self, text="Please enter details", font=("Helvetica", 14), bg='#DCDCDD')
        subtitle.pack()

        # Create Entry Fields for Patient Data
        self.first_name_entry = self.create_label_entry("First Name", label_font, entry_font)
        self.last_name_entry = self.create_label_entry("Last Name", label_font, entry_font)
        self.dob_entry = self.create_label_entry("Date of Birth", label_font, entry_font)
        self.phone_number_entry = self.create_label_entry("Phone Number", label_font, entry_font)
        self.address_entry = self.create_label_entry("Address", label_font, entry_font)
        self.last_exam_entry = self.create_label_entry("Last Exam", label_font, entry_font)

        # Create Radio Buttons for Emergent Issue and Medical Conditions
        self.emergent_issue = tk.BooleanVar(value=False)
        self.create_radio_buttons("Emergent Issue", self.emergent_issue, label_font)
        self.prescription_entry = self.create_label_entry("Prescription", label_font, entry_font)
        self.conditions = tk.BooleanVar(value=False)
        self.create_radio_buttons("Medical Conditions", self.conditions, label_font)

        # Submit Button
        submit_button = tk.Button(self, text="Submit", font=button_font, bg=button_color,
                                  command=self.submit_patient)
        submit_button.pack(pady=5)

        # Reset Button
        reset_button = tk.Button(self, text="Reset", font=button_font, bg=button_color, command=self.reset_form)
        reset_button.pack(pady=5)

        # Home Button
        home_button = tk.Button(self, text="Home", font=button_font, bg=button_color,
                                command=lambda: controller.show_frame(HomePage))
        home_button.pack(pady=5)

    def create_radio_buttons(self, label_text, variable, label_font):
        # Create a set of radio buttons for a boolean variable
        frame = tk.Frame(self, bg='#DCDCDD')
        frame.pack(pady=5)

        label = tk.Label(frame, text=label_text, font=label_font, bg='#DCDCDD')
        label.pack(side="left")

        yes_button = tk.Radiobutton(frame, text="Yes", variable=variable, value=True, bg='#DCDCDD')
        yes_button.pack(side="left")

        no_button = tk.Radiobutton(frame, text="No", variable=variable, value=False, bg='#DCDCDD')
        no_button.pack(side="left")

        return variable

    def create_label_entry(self, label_text, label_font, entry_font):
        # Create a label-entry pair for patient data
        frame = tk.Frame(self, bg='#DCDCDD')
        frame.pack(pady=5)

        label = tk.Label(frame, text=label_text, font=label_font, bg='#DCDCDD')
        label.pack(side="left")

        entry = tk.Entry(frame, font=entry_font)
        entry.pack(side="right", expand=True, fill="x")

        return entry

    def set_current_family_tree(self, family_tree_node):
        # Set the current family tree node
        self.current_family_tree = family_tree_node

    def submit_patient(self):
        # Gather data from form fields
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        dob = self.dob_entry.get()
        phone = self.phone_number_entry.get()
        address = self.address_entry.get()
        last_exam = self.last_exam_entry.get()
        emergent_issue = self.emergent_issue.get()
        prescription = self.prescription_entry.get()
        conditions = self.conditions.get()

        insurance_info = self.current_family_tree.patient.insurance_info

        try:
            # Create a new Patient object
            new_patient = Patient(first_name, last_name, dob, phone, address, last_exam, emergent_issue, prescription,
                                  conditions, insurance_info)

            # Add the new patient to the linked list
            self.linked_list.insert_patient(new_patient)

            # Check if current_family_tree is a FamilyTreeNode and add the patient
            if isinstance(self.current_family_tree, FamilyTreeNode):
                self.family_tree.add_family_member(self.current_family_tree, new_patient)
                messagebox.showinfo("Success", "New patient added to the family.")
            else:
                messagebox.showerror("Error", "No family selected for the new patient.")

            # Reset the form
            self.reset_form()

            # Now refresh the SearchPage
            search_page = self.controller.frames[SearchFamilyPage]
            search_page.refresh_family_display()

            # Navigate to SearchPage or stay on the same page based on your flow
            self.controller.show_frame(SearchFamilyPage)
        except ValueError as ve:
            messagebox.showerror("Input Error", str(ve))

    def reset_form(self):
        # Reset all form fields to empty
        self.first_name_entry.delete(0, tk.END)
        self.last_name_entry.delete(0, tk.END)
        self.dob_entry.delete(0, tk.END)
        self.phone_number_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)
        self.last_exam_entry.delete(0, tk.END)
        self.prescription_entry.delete(0, tk.END)

        # Reset radio buttons to 'no' (False)
        self.emergent_issue.set(False)
        self.conditions.set(False)


class AddNewFamilyPage(tk.Frame):
    def __init__(self, parent, controller, linked_list, family_tree):
        # Initialize the AddNewFamilyPage frame
        tk.Frame.__init__(self, parent, background='#DCDCDD')
        self.controller = controller
        self.linked_list = linked_list
        self.family_tree = family_tree

        label_font = ("Helvetica", 12)
        entry_font = ("Helvetica", 12)
        button_font = ("Helvetica", 12)
        button_color = "#C5C3C6"

        # Title and Subtitle
        title = tk.Label(self, text="Add New Family", font=("Helvetica", 16), bg='#DCDCDD')
        title.pack(pady=10)
        subtitle = tk.Label(self, text="Please enter details for the primary family member",
                            font=("Helvetica", 14), bg='#DCDCDD')
        subtitle.pack()

        # Create Entry Fields for Patient Data
        self.first_name_entry = self.create_label_entry("First Name", label_font, entry_font)
        self.last_name_entry = self.create_label_entry("Last Name", label_font, entry_font)
        self.dob_entry = self.create_label_entry("Date of Birth", label_font, entry_font)
        self.phone_number_entry = self.create_label_entry("Phone Number", label_font, entry_font)
        self.address_entry = self.create_label_entry("Address", label_font, entry_font)
        self.last_exam_entry = self.create_label_entry("Last Exam", label_font, entry_font)

        # Create Radio Buttons for Emergent Issue and Medical Conditions
        self.emergent_issue = tk.BooleanVar(value=False)
        self.create_radio_buttons("Emergent Issue", self.emergent_issue, label_font)
        self.prescription_entry = self.create_label_entry("Prescription", label_font, entry_font)
        self.conditions = tk.BooleanVar(value=False)
        self.create_radio_buttons("Medical Conditions", self.conditions, label_font)

        # Create Entry Fields for Insurance Information
        self.provider_entry = self.create_label_entry("Insurance Provider", label_font, entry_font)
        self.policy_num_entry = self.create_label_entry("Insurance Policy Number", label_font, entry_font)
        self.vision_insurance_cov = tk.BooleanVar(value=False)
        self.create_radio_buttons("Vision Insurance", self.vision_insurance_cov, label_font)
        self.medical_ins_cov = tk.BooleanVar(value=False)
        self.create_radio_buttons("Medical Insurance", self.medical_ins_cov, label_font)
        self.copay_entry = self.create_label_entry("Insurance Copay", label_font, entry_font)

        # Submit Button
        submit_button = tk.Button(self, text="Create New Family", font=button_font, bg=button_color,
                                  command=self.create_new_family)
        submit_button.pack(pady=5)

        # Button Frame
        button_frame = tk.Frame(self, bg='#DCDCDD')
        button_frame.pack(pady=5)

        # Reset and Home buttons
        reset_button = tk.Button(button_frame, text="Reset", font=button_font, bg=button_color,
                                 command=self.reset_form)
        reset_button.pack(side="left", padx=5)

        home_button = tk.Button(button_frame, text="Home", font=button_font, bg=button_color,
                                command=lambda: controller.show_frame(HomePage))
        home_button.pack(side="left", padx=5)

    def create_radio_buttons(self, label_text, variable, label_font):
        # Create a set of radio buttons for a boolean variable
        frame = tk.Frame(self, bg='#DCDCDD')
        frame.pack(pady=5)

        label = tk.Label(frame, text=label_text, font=label_font, bg='#DCDCDD')
        label.pack(side="left")

        yes_button = tk.Radiobutton(frame, text="Yes", variable=variable, value=True, bg='#DCDCDD')
        yes_button.pack(side="left")

        no_button = tk.Radiobutton(frame, text="No", variable=variable, value=False, bg='#DCDCDD')
        no_button.pack(side="left")

        return variable

    def create_label_entry(self, label_text, label_font, entry_font):
        # Create a label-entry pair for patient data
        frame = tk.Frame(self, bg='#DCDCDD')
        frame.pack(pady=5)

        label = tk.Label(frame, text=label_text, font=label_font, bg='#DCDCDD')
        label.pack(side="left")

        entry = tk.Entry(frame, font=entry_font)
        entry.pack(side="right", expand=True, fill="x")

        return entry

    def create_new_family(self):
        # Gather data from form fields
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        dob = self.dob_entry.get()
        phone = self.phone_number_entry.get()
        address = self.address_entry.get()
        last_exam = self.last_exam_entry.get()
        emergent_issue = self.emergent_issue.get()
        prescription = self.prescription_entry.get()
        conditions = self.conditions.get()
        primary_member = first_name + " " + last_name
        provider_name = self.provider_entry.get()
        policy_number = self.policy_num_entry.get()
        vision_coverage = self.vision_insurance_cov.get()
        medical_coverage = self.medical_ins_cov.get()
        copay = self.copay_entry.get()

        try:
            # Create a new InsuranceInformation object
            new_insurance = InsuranceInformation(primary_member, provider_name, policy_number, vision_coverage,
                                                 medical_coverage, copay)

            # Create a new Patient object
            new_patient = Patient(first_name, last_name, dob, phone, address, last_exam, emergent_issue,
                                  prescription, conditions, new_insurance)

            # Insert the new patient into the linked list
            self.linked_list.insert_patient(new_patient)

            # Create a new family and add it to the family tree
            new_family_node = self.family_tree.add_family(new_patient, new_insurance)

            # Display confirmation message
            messagebox.showinfo("Success", "New family created with the patient as the primary member.")

            # Reset the form
            self.reset_form()

            # Navigate to SearchPage and display the new family's information
            search_page = self.controller.frames[SearchFamilyPage]
            self.controller.show_frame(SearchFamilyPage)
            search_page.display_family_info(new_family_node)
        except ValueError as ve:
            messagebox.showerror("Input Error", str(ve))

    def reset_form(self):
        # Reset all form fields to empty
        self.first_name_entry.delete(0, tk.END)
        self.last_name_entry.delete(0, tk.END)
        self.dob_entry.delete(0, tk.END)
        self.phone_number_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)
        self.last_exam_entry.delete(0, tk.END)
        self.prescription_entry.delete(0, tk.END)

        self.provider_entry.delete(0, tk.END)
        self.policy_num_entry.delete(0, tk.END)
        self.copay_entry.delete(0, tk.END)

        # Reset radio buttons to 'no' (False)
        self.emergent_issue.set(False)
        self.conditions.set(False)
        self.vision_insurance_cov.set(False)
        self.medical_ins_cov.set(False)


class ScheduleAppointmentPage(tk.Frame):
    def __init__(self, parent, controller, linked_list, family_tree):
        # Initialize the ScheduleAppointmentPage frame
        tk.Frame.__init__(self, parent, background='#DCDCDD')
        self.controller = controller
        self.linked_list = linked_list
        self.family_tree = family_tree
        self.appointment_scheduler = AppointmentScheduler()

        # Title and Subtitle
        title = tk.Label(self, text="Patients to Schedule", font=("Helvetica", 16), bg='#DCDCDD')
        title.pack(pady=10)
        subtitle = tk.Label(self, text="Patients are sorted by priority.", font=("Helvetica", 14), bg='#DCDCDD')
        subtitle.pack()

        # Create a container for the patient list
        self.patient_list_container = tk.Frame(self, background='#DCDCDD')
        self.patient_list_container.pack(fill="both", expand=True)

        # Load and display patients when the page is shown
        self.load_and_display_patients()

        # Home Button
        home_button = tk.Button(self, text="Home", command=lambda: controller.show_frame(HomePage))
        home_button.pack(pady=5)

    def load_and_display_patients(self):
        # Clear existing patient list
        for widget in self.patient_list_container.winfo_children():
            widget.destroy()

        # Add patients from the linked list to the priority queue
        current = self.linked_list.head
        while current:
            self.appointment_scheduler.add_patient(current)
            current = current.next

        # Get and display all patients
        for patient in self.appointment_scheduler.get_all_patients():
            if patient.priority_level < 4:
                patient_info = f"{patient.first_name} {patient.last_name}, DOB: {patient.dob}, " \
                               f"Priority: {patient.priority_level}"
                tk.Label(self.patient_list_container, text=patient_info).pack()

    def refresh_page(self):
        self.load_and_display_patients()


class ViewAllPatientsPage(tk.Frame):
    def __init__(self, parent, controller, linked_list, family_tree):
        # Initialize the ViewAllPatientsPage frame
        tk.Frame.__init__(self, parent, background='#DCDCDD')
        self.controller = controller
        self.linked_list = linked_list
        self.family_tree = family_tree

        # Title and Subtitle
        title = tk.Label(self, text="Patients List", font=("Helvetica", 16), bg='#DCDCDD')
        title.pack(pady=10)
        subtitle = tk.Label(self, text="Patients are sorted alphabetically.", font=("Helvetica", 14), bg='#DCDCDD')
        subtitle.pack()

        # Create a container for the patient list
        self.patient_list_container = tk.Frame(self, background='#DCDCDD')
        self.patient_list_container.pack(fill="both", expand=True)

        # Load and display patients when the page is shown
        self.load_and_display_patients()

        # Home Button
        home_button = tk.Button(self, text="Home", command=lambda: controller.show_frame(HomePage))
        home_button.pack(pady=5)

    def load_and_display_patients(self):
        # Clear existing patient list
        for widget in self.patient_list_container.winfo_children():
            widget.destroy()

        # Extract patients from the linked list and sort them alphabetically
        patients = []
        current = self.linked_list.head
        while current:
            patients.append(current)
            current = current.next

        patients.sort(key=lambda patient: (patient.last_name, patient.first_name))

        # Display sorted patients
        for patient in patients:
            patient_info = f"{patient.first_name} {patient.last_name}, DOB: {patient.dob}"
            tk.Label(self.patient_list_container, text=patient_info).pack()

    def refresh_page(self):
        self.load_and_display_patients()
