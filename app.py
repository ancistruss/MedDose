from models.card import MedicineCard
from db import get_connection

class App:
    def __init__(self):
        pass

    def search(self, name):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT name, description, interactions FROM medicines WHERE lower(name)=lower(?)", (name,))
        row = cur.fetchone()
        conn.close()

        if row:
            name, description, interactions = row
            inter_list = interactions.split(",") if interactions else []
            return MedicineCard(name, description, inter_list)

        return None

    def get_info(self, name):
        card = self.search(name)
        if not card:
            return None
        return {
            "name": card.name,
            "description": card.description,
            "interactions": card.interactions
        }

    def check_compatibility(self, med1, med2):
        card1 = self.search(med1)
        card2 = self.search(med2)

        if not card1 or not card2:
            return False, "Один із препаратів не знайдено"

        ok1 = card1.is_compatible_with(med2)
        ok2 = card2.is_compatible_with(med1)

        return ok1 and ok2, "Перевірка виконана"
