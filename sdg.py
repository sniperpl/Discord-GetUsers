import tkinter as tk
import tkinter.font as tkFont

def update_preview(event=None):
    selected_font = font_listbox.get(tk.ACTIVE)
    preview_font = tkFont.Font(family=selected_font, size=16)
    preview_label.config(font=preview_font, text=f"To jest: {selected_font}")

root = tk.Tk()
root.title("Podgląd czcionek")

# Pobierz i posortuj dostępne czcionki
fonts = sorted(tkFont.families())

# Listbox z czcionkami
font_listbox = tk.Listbox(root, height=20, width=30)
for f in fonts:
    font_listbox.insert(tk.END, f)
font_listbox.pack(side=tk.LEFT, padx=10, pady=10)
font_listbox.bind("<<ListboxSelect>>", update_preview)

# Podgląd czcionki
preview_label = tk.Label(root, text="Wybierz czcionkę z listy", width=40, height=10)
preview_label.pack(side=tk.RIGHT, padx=10, pady=10)

root.mainloop()