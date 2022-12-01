from fpdf import FPDF
from trame import *
from liste_trames import *

class PDF(FPDF):
	def header(self):
		self.set_font("Helvetica", "B", size = 20)
		self.set_line_width(1)
		self.cell(0, 10, "FRAMES ANALYSIS", new_x = "LMARGIN", new_y = "NEXT", align = "C", border = "B")
		self.ln(10)

	def footer(self):
		self.set_y(-15)
		self.set_font("Helvetica", size = 10)
		self.cell(0, 10, f"{self.page_no()}/{{nb}}", align = "R")

	def print_frame_title(self, iden):
		self.set_font("Helvetica", "B", size = 14)
		self.cell(0, 10, txt = "TRAME #{0:04d}".format(iden), new_x = "LMARGIN", new_y = "NEXT")
		self.ln(5)

	def print_multi_cell(self, string):
		self.set_draw_color(46, 59, 67)
		self.set_font("Helvetica", size = 12)
		self.set_line_width(1)
		self.multi_cell(0, 10, txt = string, border = "L", new_x = "LMARGIN")
		self.ln(5)
		

def create_pdf(filename, trame_liste):
	pdf = PDF(orientation = "P", unit = "mm", format = "A4")
	pdf.set_title("FRAMES ANALYSIS")
	pdf.set_author("WireLinks 1.0.0")

	pdf.add_page()
	pdf.set_auto_page_break(auto = True, margin = 15)

	for trame in trame_liste:
		pdf.print_frame_title(trame.get_iden())
		pdf.print_multi_cell("test")
		
	if not filename.endswith(".pdf"):
		filename += ".pdf"	

	pdf.output(filename)
