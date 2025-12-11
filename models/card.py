class MedicineCard:
    def __init__(self, name, description, interactions=None):
        self.name = name
        self.description = description
        self.interactions = interactions or []

    def is_compatible_with(self, other_name):
        # Порівняння без урахування регістру
        other_name = other_name.lower()
        interactions = [i.lower() for i in self.interactions]
        return other_name not in interactions

    def __str__(self):
        return f"MedicineCard(name={self.name}, interactions={self.interactions})"
