import time
from fpdf import FPDF


class Card(FPDF):
    
    date_size: float = 15
    normal_size: float = 14

    def __init__(self):
        super().__init__('L', unit = "mm", format = "A4")
        self.set_font('Times', '', self.normal_size)
        self.set_margins(10,15,10)

    def header(self):
        self.set_font_size(self.date_size)
        local_time = time.localtime()
        self.cell(0,0,f'{local_time.tm_mday}/{local_time.tm_mon}/{local_time.tm_year}',0,0,'R')
        self.ln()

    def fill(self, content: str):
        self.set_font('Times', '', self.normal_size)
        self.add_page()
        self.set_auto_page_break(True, 20)
        text_width = self.w - self.l_margin - self.r_margin
        self.multi_cell(text_width,8,content,0,'J')

    def footer(self):
        self.ln()
        self.ln()