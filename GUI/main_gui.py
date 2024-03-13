

import customtkinter as tk

tk.set_appearance_mode("System")  # Modes: system (default), light, dark
tk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

root = tk.CTk()  # create CTk window like you do with the Tk window
root.geometry("400x240")

def button_function():
    print("stuff printed")

# Use CTkButton instead of tkinter Button
button = tk.CTkButton(master=root, text="Print Stuff", command=button_function)
button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

root.mainloop()