import os

from model.card import Card



class PdfService:
    def generate_card(self, content: str, filename: str):
        folder = os.getenv('USER_DATA_DIR', os.path.join(os.getcwd(),'user_data','presentation_cards'))
        if not os.path.exists(folder):
            os.mkdir(folder)
        card = Card()
        card.fill(content)
        card.set_author('github.com/katarem/jobby')
        card.output(os.path.join(folder, filename))
        