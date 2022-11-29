from tkinter import messagebox as mb

def type_error(layer, typ, n):
	mb.showwarning("Warning", f"Unfortunately, WireLinks cannot analyze the {layer}-layer protocol: {typ} used\
 in the frame #{n:04}")
