class User:
    def __init__(self, username):
        self.username = username
        self.saved_cards = []

    def add_card(self, card):
        self.saved_cards.append(card)

    def __str__(self):
        return f"User(username={self.username}, saved_cards={len(self.saved_cards)})"
