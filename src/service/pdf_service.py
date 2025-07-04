import os

from fpdf import FPDF

from model.card import Card
from model.config import Config


class PdfService:
    def test(self, content: str):
        file = os.getenv('USER_DATA_DIR', os.path.join(os.getcwd(),'user_data','hola.pdf'))
        card = Card()
        card.fill(content)
        card.set_author('github.com/katarem/jobby')
        card.output(file)
        