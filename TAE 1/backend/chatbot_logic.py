import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "hospital.db")

class ChatbotLogic:
    def __init__(self):
        # Symptom-to-Department mapping
        self.symptom_map = {
            "chest pain": "Cardiology",
            "heartbeat": "Cardiology",
            "palpitations": "Cardiology",
            "blood pressure": "Cardiology",
            "bone pain": "Orthopedics",
            "fracture": "Orthopedics",
            "joint pain": "Orthopedics",
            "leg pain": "Orthopedics",
            "headache": "Neurology",
            "seizures": "Neurology",
            "dizzy": "Neurology",
            "numbness": "Neurology"
        }

    def get_greeting(self, user_input):
        greetings = ["hello", "hi", "hey", "greetings"]
        if any(word in user_input.lower() for word in greetings):
            return "Hello! Welcome to Engineering Hospital. I'll help you book an appointment. Would you like to use our **Symptom Checker** or **Book Directly**? (Just tell me your name first!)"
        return None

    def suggest_department(self, user_input):
        lowered = user_input.lower()
        for symptom, dept in self.symptom_map.items():
            if symptom in lowered:
                return dept
        return None

    def validate_name(self, name):
        return len(name.strip()) >= 2

    def validate_age(self, age):
        try:
            val = int(age)
            return 1 <= val <= 120
        except ValueError:
            return False

    def validate_mobile(self, mobile):
        # Strict 10-digit validation
        stripped = str(mobile).strip()
        return len(stripped) == 10 and stripped.isdigit()

    def get_departments(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT department FROM Doctors")
        deps = [row[0] for row in cursor.fetchall()]
        conn.close()
        return deps

    def get_doctors_by_department(self, department):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM Doctors WHERE department = ?", (department,))
        doctors = [{"id": row[0], "name": row[1]} for row in cursor.fetchall()]
        conn.close()
        return doctors

    def get_availability(self, doctor_id):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT slot FROM Availability WHERE doctor_id = ? AND is_booked = 0", (doctor_id,))
        slots = [row[0] for row in cursor.fetchall()]
        conn.close()
        return slots

    def book_appointment(self, patient_data, doctor_id, slot):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Save Patient
        cursor.execute("INSERT INTO Patients (name, age, mobile) VALUES (?, ?, ?)", 
                       (patient_data['name'], patient_data['age'], patient_data['mobile']))
        patient_id = cursor.lastrowid
        
        # Check if slot already booked
        cursor.execute("SELECT is_booked FROM Availability WHERE doctor_id = ? AND slot = ?", (doctor_id, slot))
        row = cursor.fetchone()
        if not row or row[0] == 1:
            conn.close()
            return None # Already booked or invalid
        
        # Create Appointment
        cursor.execute("INSERT INTO Appointments (patient_id, doctor_id, slot, date) VALUES (?, ?, ?, date('now'))",
                       (patient_id, doctor_id, slot))
        
        # Mark slot as booked
        cursor.execute("UPDATE Availability SET is_booked = 1 WHERE doctor_id = ? AND slot = ?", (doctor_id, slot))
        
        conn.commit()
        conn.close()
        return True
