from queue import PriorityQueue
import time


class AppointmentScheduler:
    def __init__(self):
        # Initialize the AppointmentScheduler
        self.queue = PriorityQueue()  # Priority queue to store patients
        self.counter = 0  # Initialize a counter to break ties

    def add_patient(self, patient):
        # Add a patient to the priority queue with priority based on their priority level, arrival time, and counter
        timestamp = time.time()  # Get the current time as a timestamp
        self.queue.put((patient.priority_level, timestamp, self.counter, patient))
        self.counter += 1  # Increment the counter for the next patient

    def get_all_patients(self):
        # Retrieve and return all patients from the priority queue, sorted by priority, arrival time, and counter
        patients = []
        while not self.queue.empty():
            _, _, _, patient = self.queue.get()
            patients.append(patient)
        return patients
