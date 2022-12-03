import os
import sys

import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from tkinter import simpledialog as sd
import tkinter.font as tkFont
import tkmacosx

from trame import *
from liste_trames import *

sys.path.append("../lib")
from readingTools import *
from writingTools import *


if sys.platform == "win32":
	from ctypes import windll
	windll.shcore.SetProcessDpiAwareness(1)


root = tk.Tk()

# Window's Parameters Configuration
app_name = "WireLinks 1.0.0"
dirname = os.path.dirname(__file__)


# Default configuration

window_width = 1280
window_height = 720
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width / 2 - window_width / 2)
center_y = int(screen_height / 2 - window_height / 2)

root.iconphoto(False, tk.PhotoImage(file = os.path.join(dirname, "../icons/logo.png")))

root.title(app_name)
root.minsize(720, 480)
root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")


# Fonts and Colors
title_font = tkFont.Font(family = "Roboto Medium", size = 18)
subtitle_font = tkFont.Font(family = "Roboto Medium", size = 13)
text_font = tkFont.Font(family = "Roboto", size = 12)
button_font = tkFont.Font(family = "Roboto Medium", size = 12)
entry_font = tkFont.Font(family = "Roboto", size = 12, slant = "italic")

menu_color = "#292927"
bg_color = "#5b524b"
frame_color = "#292927"
entry_color = "#ffffff"
hover_menu_color = "#5b524b"
hover_listbox_color = "#5b524b"
hover_button_color = "#292927"
text_color = "#ffffff"


# Grid for the main frame
root.configure(bg = bg_color)
root.columnconfigure(1, weight = 2)
root.rowconfigure(0, weight = 1)


# Menu and Content Frames
menu = tk.Frame(root, bg = menu_color)
menu.grid(column = 0, row = 0, sticky = tk.NS)

right_frame = tk.Frame(root)
right_frame.grid(padx = 125, pady = 20, column = 1, row = 0, sticky = "new")
right_frame.columnconfigure(0, weight = 1)
right_frame.rowconfigure(0, weight = 1)
right_frame.rowconfigure(1, weight = 10000)

frames_for_pdf = []


# Menu Buttons

# Open File Dialog
filetypes = [("Text Files (*.txt)", "*.txt")]

def file_dialog_command():
	tracefile_name = fd.askopenfilename(title = "Choose your File", filetypes = filetypes, initialdir = "../" + dirname)
	if(tracefile_name != ""):
		content_frames.delete(1, tk.END)
		trames = get_frames(tracefile_name)
		TrameList.set_liste([])

		for i in range(len(trames)):
			TrameList(Trame(i+1, trames[i]))
	
		if (len(TrameList.get_liste()) == 0):
			mb.showinfo("Info", "Empty File or No Valid Frame was Found")

		else:
			for i in TrameList.get_liste():
				add_frame(i.afficher_info_imp_gui())
				frames_for_pdf.append(i)

folder_icon = tk.PhotoImage(file = os.path.join(dirname, "../icons/folder-open.png"))
file_dialog = tkmacosx.Button(menu, bg = menu_color, fg = text_color, bd = 5, height = 80, width = 80, relief = tk.FLAT, 
								borderless = True, activebackground = menu_color, activeforeground = text_color, overbackground = hover_menu_color,
								focusthickness = 0, image = folder_icon, command = lambda: file_dialog_command())
file_dialog.pack()


# Export to PDF
def is_invalid_filename(filename):
	invalid_characters = ["/", "\\", ":", "*", "?", "\"", "<", ">", "|"]
	
	for character in invalid_characters:
		if character in filename:
			return True

def save_command():
	answer = mb.askyesno("Confirmation", "Do you want to save the analysis of the frames ?")

	if answer:
		if frames_for_pdf != []:
			filename = sd.askstring("Input", "Enter a filename")
			if filename != None:
				if is_invalid_filename(filename):
					mb.showerror("Error", "Invalid Filename")
				else:
					filename = "../" + filename
					create_pdf(filename, frames_for_pdf)

		else:
			mb.showerror("Error", "There is no relevant frame to save")

save_icon = tk.PhotoImage(file = os.path.join(dirname, "../icons/save.png"))
save_btn = tkmacosx.Button(menu, bg = menu_color, fg = text_color, bd = 5, height = 80, width = 80, relief = tk.FLAT, 
								borderless = True, activebackground = menu_color, activeforeground = text_color, overbackground = hover_menu_color,
								focusthickness = 0, image = save_icon, command = lambda: save_command())
save_btn.pack()

# Exit
def exit_command():
	answer = mb.askyesno("Confirmation", "Are you sure that you want to quit {0} ?".format(app_name))
	if answer:
		root.destroy()

exit_icon = tk.PhotoImage(file = os.path.join(dirname, "../icons/exit.png"))
exit_btn = tkmacosx.Button(menu, bg = menu_color, fg = text_color, bd = 5, height = 80, width = 80, relief = tk.FLAT, 
								borderless = True, activebackground = menu_color, activeforeground = text_color, overbackground = hover_menu_color,
								focusthickness = 0, image = exit_icon, command = lambda: exit_command())
exit_btn.pack()


def handle_filters(e):
	filtre = filterbar.get()
	content_frames.delete(1, tk.END)

  # Traitement du filtre
	if(filtre.replace(" ", "") == ""):
		if(len(TrameList.get_liste()) == 0):
			mb.showinfo("Info", "The file doesn't have any relevant frame")

		else:
			for i in range(len(frames_for_pdf)):
				del frames_for_pdf[0]

			for i in TrameList.get_liste():
				add_frame(i.afficher_info_imp_gui())
				frames_for_pdf.append(i)

	else:
		for i in range(len(frames_for_pdf)):
			del frames_for_pdf[0]
			
		liste_filtre = TrameList.filtre(filtre)
		for i in liste_filtre:
			add_frame(i.afficher_info_imp_gui())
			frames_for_pdf.append(i)


# Entry for Filters

def on_focus_in(entry):
	if entry.cget("state") == "disabled":
		entry.config(state = "normal", font = text_font)
		entry.delete(0, "end")

def on_focus_out(entry, placeholder):
	if entry.get() == "":
		entry.insert(0, placeholder)
		entry.config(state = "disabled", font = entry_font)

filterbar = tk.Entry(right_frame, bg = menu_color, disabledbackground = menu_color, fg = entry_color, 
							relief = tk.FLAT, disabledforeground = entry_color, bd = 0, font = entry_font)
filterbar.insert(0, " Type your Filter")
filterbar.configure(state = "disabled")
filterbar.grid(row = 0, sticky = tk.EW)

# Placeholder
filterbar_focus_in = filterbar.bind("<Button-1>", lambda x: on_focus_in(filterbar))
filterbar_focus_out = filterbar.bind("<FocusOut>", lambda x: on_focus_out(filterbar, " Type your Filter"))
filterbar.bind("<Return>", handle_filters)


# Content
content = tk.Frame(right_frame, bg = bg_color)
content.grid(row = 1, sticky = tk.EW)
#content_title = tk.Label(content, bg = bg_color, font = title_font, fg = text_color, text = "FRAMES ANALYSIS")
#content_title.pack(pady = (50, 25))


# List of Frames

# Wrapper and Listbox
#frames_subtitle = tk.Label(content, bg = bg_color, font = subtitle_font, fg = text_color, text = "List of Frames")
#frames_subtitle.pack(anchor = "w")

printable_frames_list = [("   {:<4d}" + (8 - len(str(0))) * " " + "{:<20s}" + 15 * " " + "{:<20s}" + 15 * " " + "{:<15s}" + 20 * " " + "{:<15s}" + 15 * " " + "{:<10s}" + 20 * " " + "{:<2s}" + 20 * " " + "{:<2s}" + 20 * " " + "{:<3s}").format(0, "Src MAC", "Dst MAC", "Src IP", "Dst IP", "Protocol", "Src Port", "Dst Port", "Info")]
tk_printable_frames_list = tk.Variable(value = printable_frames_list)
frames_wrapper = tk.Frame(content, relief = tk.GROOVE, highlightthickness = 0, highlightbackground = frame_color)
frames_wrapper.pack(pady = (50,0), fill = tk.BOTH)

content_frames = tk.Listbox(frames_wrapper, bg = frame_color, fg = text_color, height = 13, listvariable = tk_printable_frames_list, 
									selectmode = tk.SINGLE, font = text_font, activestyle = "none", relief = tk.FLAT, highlightthickness = 0,
									selectbackground = hover_listbox_color)

def add_frame(trame):
	content_frames.insert(tk.END, trame)


# Scrollbars
frames_scrollbar = tk.Scrollbar(frames_wrapper, orient = "vertical", width = 15)
frames_scrollbar.pack(side = "right", fill = "y")

frames_scrollbar_hor = tk.Scrollbar(frames_wrapper, orient = "horizontal", width = 15)
frames_scrollbar_hor.pack(side = "bottom", fill = "x")

content_frames.config(yscrollcommand = frames_scrollbar.set)
frames_scrollbar.config(command = content_frames.yview)
content_frames.config(xscrollcommand = frames_scrollbar_hor.set)
frames_scrollbar_hor.config(command = content_frames.xview)

content_frames.pack(fill = tk.BOTH)


# Details

# Wrapper and Text Widget
#text_subtitle = tk.Label(content, bg = bg_color, font = subtitle_font, fg = text_color, text = "Details")
#text_subtitle.pack(anchor = "w")

text_wrapper = tk.Frame(content, relief = tk.GROOVE, highlightthickness = 0, highlightcolor = hover_listbox_color)
text_wrapper.pack(pady = (50,0), fill = tk.BOTH)

content_text = tk.Text(text_wrapper, bg = frame_color, fg = text_color, height = screen_height, font = text_font,
	relief = tk.FLAT, highlightthickness = 0)


# Scrollbars
text_scrollbar = tk.Scrollbar(text_wrapper, orient = "vertical", width = 15)
text_scrollbar.pack(side = "right", fill = "y")

text_scrollbar_hor = tk.Scrollbar(text_wrapper, orient = "horizontal", width = 15)
text_scrollbar_hor.pack(side = "bottom", fill = "x")

content_text.config(yscrollcommand = text_scrollbar.set)
text_scrollbar.config(command = content_text.yview)
content_text.config(xscrollcommand = text_scrollbar_hor.set)
text_scrollbar_hor.config(command = content_text.xview)

content_text.pack(fill = tk.BOTH, side = "left", expand = tk.YES)
content_text.config(state = "disabled")

def toggle_all():
	for widget in content_text.winfo_children():
		widget.destroy()

	content_text.config(state = "normal")
	content_text.delete("1.0", tk.END)
	
	trame = get_selection()
	button_display()

	if trame == []:
		content_text.config(state = "disabled")
		return
	
	content_text.config(state = "normal")
	if (trame.get_ethernet() != None):
		content_text.insert(tk.END, trame.get_ethernet())
		content_text.insert(tk.END, "\n\n")

		if (trame.get_ip() != None):
			content_text.insert(tk.END, trame.get_ip())
			content_text.insert(tk.END, "\n\n")

			if (trame.get_transport() != None):
				content_text.insert(tk.END, trame.get_transport())
				content_text.insert(tk.END, "\n\n")

				if (trame.get_http() != None):
					content_text.insert(tk.END, trame.get_http())

					if (trame.get_data() != None):
						content_text.insert(tk.END, "\n\n")
						content_text.insert(tk.END, trame.get_data())

				elif (trame.get_data() != None):
					content_text.insert(tk.END, trame.get_data())

	content_text.config(state = "disabled")


def toggle_ethernet():
	for widget in content_text.winfo_children():
		widget.destroy()

	content_text.config(state = "normal")
	content_text.delete("1.0", tk.END)

	trame = get_selection()
	button_display()

	if (trame.get_ethernet() != None):
		content_text.config(state = "normal")
		content_text.insert(tk.END, trame.get_ethernet())

	content_text.config(state = "disabled")


def toggle_ip():
	for widget in content_text.winfo_children():
		widget.destroy()

	content_text.config(state = "normal")
	content_text.delete("1.0", tk.END)

	trame = get_selection()
	button_display()

	if (trame.get_ip() != None):
		content_text.config(state = "normal")
		content_text.insert(tk.END, trame.get_ip())

	content_text.config(state = "disabled")


def toggle_arp():
	for widget in content_text.winfo_children():
		widget.destroy()

	content_text.config(state = "normal")
	content_text.delete("1.0", tk.END)

	trame = get_selection()
	button_display()

	if (trame.get_arp() != None):
		content_text.config(state = "normal")
		content_text.insert(tk.END, trame.get_ip())

	content_text.config(state = "disabled")


def toggle_transport():
	for widget in content_text.winfo_children():
		widget.destroy()

	content_text.config(state = "normal")
	content_text.delete("1.0", tk.END)

	trame = get_selection()
	button_display()

	if (trame.get_transport() != None):
		content_text.config(state = "normal")
		content_text.insert(tk.END, trame.get_transport())

	content_text.config(state = "disabled")


def toggle_http():
	for widget in content_text.winfo_children():
		widget.destroy()

	content_text.config(state = "normal")
	content_text.delete("1.0", tk.END)

	trame = get_selection()
	button_display()

	if (trame.get_http() != None):
		content_text.config(state = "normal")
		content_text.insert(tk.END, trame.get_http())

	content_text.config(state = "disabled")


def toggle_data():
	for widget in content_text.winfo_children():
		widget.destroy()

	content_text.config(state = "normal")
	content_text.delete("1.0", tk.END)

	trame = get_selection()
	button_display()

	if (trame.get_data() != None):
		content_text.config(state = "normal")
		content_text.insert(tk.END, trame.get_data())

	content_text.config(state = "disabled")


def button_display():
	trame = get_selection()
	content_text.config(state = "normal")

	if trame == None or trame == []:
		content_text.config(state = "disabled")
		return

	all_button = tkmacosx.Button(content_text, bg = bg_color, fg = text_color, bd = 5, height = 25, relief = tk.FLAT, width = 175,
							borderless = True, activebackground = menu_color, activeforeground = text_color, overbackground = hover_button_color,
							focusthickness = 0, font = button_font, text = "ALL", command = lambda: toggle_all())
	content_text.window_create(tk.END, window = all_button)
	content_text.insert(tk.END, "   ")

	if (trame.get_ethernet() != None):
		eth_button = tkmacosx.Button(content_text, bg = bg_color, fg = text_color, bd = 5, height = 25, relief = tk.FLAT, width = 175,
							borderless = True, activebackground = menu_color, activeforeground = text_color, overbackground = hover_button_color,
							focusthickness = 0, font = button_font, text = "Ethernet II", command = lambda: toggle_ethernet())
		content_text.window_create(tk.END, window = eth_button)
		content_text.insert(tk.END, "   ")

		if (trame.get_ip() != None):
			ip_button = tkmacosx.Button(content_text, bg = bg_color, fg = text_color, bd = 5, height = 25, relief = tk.FLAT, width = 175,
							borderless = True, activebackground = menu_color, activeforeground = text_color, overbackground = hover_button_color,
							focusthickness = 0, font = button_font, text = trame.ethernet.get_type_eth2(), command = lambda: toggle_ip())
			content_text.window_create(tk.END, window = ip_button)
			content_text.insert(tk.END, "   ")

			if (trame.get_transport() != None):
				tcp_button = tkmacosx.Button(content_text, bg = bg_color, fg = text_color, bd = 5, height = 25, relief = tk.FLAT, width = 175,
							borderless = True, activebackground = menu_color, activeforeground = text_color, overbackground = hover_button_color,
							focusthickness = 0, font = button_font, text = trame.get_transport().get_typ(), command = lambda: toggle_transport())
				content_text.window_create(tk.END, window = tcp_button)
				content_text.insert(tk.END, "   ")

				if (trame.get_http() != None):
					http_button = tkmacosx.Button(content_text, bg = bg_color, fg = text_color, bd = 5, height = 25, relief = tk.FLAT, width = 175,
							borderless = True, activebackground = menu_color, activeforeground = text_color, overbackground = hover_button_color,
							focusthickness = 0, font = button_font, text = "HTTP", command = lambda: toggle_http())
					content_text.window_create(tk.END, window = http_button)
					content_text.insert(tk.END, "   ")

	if (trame.get_data() != None):
		data_button = tkmacosx.Button(content_text, bg = bg_color, fg = text_color, bd = 5, height = 25, relief = tk.FLAT, width = 175,
			borderless = True, activebackground = menu_color, activeforeground = text_color, overbackground = hover_button_color,
			focusthickness = 0, font = button_font, text = "Data", command = lambda: toggle_data())
		content_text.window_create(tk.END, window = data_button)
		content_text.insert(tk.END, "   ")

	content_text.insert(tk.END, "\n\n")
	content_text.config(state = "disabled")


def on_selected(e):
	for widget in content_text.winfo_children():
		widget.destroy()

	content_text.config(state = "normal")
	content_text.delete("1.0", tk.END)

	button_display()
	toggle_all()
	content_text.config(state = "disabled")
	

def get_selection():
	if content_frames.curselection() == ():
		return []

	i = content_frames.curselection()[0]

	if (i != 0):
		return TrameList.get_trame(i)
	else:
		return []			

content_frames.bind('<<ListboxSelect>>', on_selected)

root.mainloop()