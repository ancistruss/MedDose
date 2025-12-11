import sqlite3

DB_NAME = "medicines.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS medicines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            description TEXT,
            interactions TEXT
        )
    """)

    conn.commit()
    conn.close()


def add_default_data():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM medicines")
    count = cur.fetchone()[0]

    if count > 0:
        conn.close()
        return

    meds = [
        ("Aspirin", "Знеболювальний", "Ibuprofen,Warfarin,Prednisone"),
        ("Ibuprofen", "Протизапальний", "Aspirin,Prednisone"),
        ("Paracetamol", "Жарознижувальний", ""),
        ("Warfarin", "Антикоагулянт", "Aspirin,Metronidazole,Fluconazole"),
        ("Amoxicillin", "Антибіотик", ""),
        ("Caffeine", "Стимулятор ЦНС", "Sedatives"),
        ("Cetirizine", "Протиалергічний", "Alcohol"),
        ("Diphenhydramine", "Антигістамінний", "Alcohol,Caffeine"),
        ("Omeprazole", "Інгібітор протонної помпи", "Ketoconazole,Itraconazole"),
        ("Metformin", "Препарат для діабету", "Alcohol"),
        ("Prednisone", "Гормональний протизапальний", "Ibuprofen,Aspirin"),
        ("Alcohol", "Етанол (сильна взаємодія з багатьма препаратами)",
         "Metformin,Diphenhydramine,Cetirizine"),
        ("Metronidazole", "Антибіотик від інфекцій", "Alcohol,Warfarin"),
        ("Fluconazole", "Протигрибковий", "Warfarin"),
        ("Ketoconazole", "Протигрибковий", "Omeprazole"),
        ("Itraconazole", "Протигрибковий", "Omeprazole"),
        ("Diazepam", "Седативний/протисудомний", "Alcohol,Caffeine"),
        ("Sertraline", "Антидепресант", "Tramadol,MAOI"),
        ("Tramadol", "Знеболювальний наркотичний", "Sertraline,MAOI"),
        ("MAOI", "Інгібітори моноаміноксидази", "Sertraline,Tramadol"),
        ("Lisinopril", "Препарат від тиску", "Ibuprofen"),
        ("Losartan", "Препарат від тиску", "Ibuprofen"),
        ("Azithromycin", "Антибіотик", ""),
        ("Clarithromycin", "Антибіотик", "Warfarin"),
        ("Insulin", "Гормональний засіб при діабеті", "Alcohol")
    ]

    cur.executemany("""
        INSERT INTO medicines (name, description, interactions)
        VALUES (?, ?, ?)
    """, meds)

    conn.commit()
    conn.close()
