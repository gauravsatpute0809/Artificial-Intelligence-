import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "hospital.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Patients table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            mobile TEXT NOT NULL
        )
    ''')

    # Doctors table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL
        )
    ''')

    # Availability table (Simulated slots)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Availability (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doctor_id INTEGER,
            slot TEXT NOT NULL,
            is_booked BOOLEAN DEFAULT 0,
            FOREIGN KEY (doctor_id) REFERENCES Doctors(id)
        )
    ''')

    # Appointments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            doctor_id INTEGER,
            slot TEXT NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY (patient_id) REFERENCES Patients(id),
            FOREIGN KEY (doctor_id) REFERENCES Doctors(id)
        )
    ''')

    # Seed initial data if Doctors table is empty
    cursor.execute("SELECT COUNT(*) FROM Doctors")
    if cursor.fetchone()[0] == 0:
        doctors = [
            ("Dr. Sharma", "Cardiology"),
            ("Dr. Mehta", "Cardiology"),
            ("Dr. Patil", "Orthopedics"),
            ("Dr. Rao", "Neurology")
        ]
        cursor.executemany("INSERT INTO Doctors (name, department) VALUES (?, ?)", doctors)
        
        # Seed availability for each doctor
        slots = ["09:00 AM", "10:30 AM", "12:00 PM", "02:30 PM", "04:00 PM"]
        for i in range(1, 5): # 4 doctors
            for slot in slots:
                cursor.execute("INSERT INTO Availability (doctor_id, slot) VALUES (?, ?)", (i, slot))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database Initialized Successfully!")
