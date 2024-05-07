import numpy as np
import matplotlib.pyplot as plt
from tkinter import filedialog
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Initialize a list to hold the coordinates
coordinates = []

file_path = filedialog.askopenfilename()
# Open the G-code file
with open(file_path, 'r') as file:
    i = 0
    x = 0
    y = 0
    z = 0
    for line in file:
        if i < 44:
            i += 1
            continue
        if line.startswith(';TIME_ELAPSED'):
            break
        if line.startswith('G0') or line.startswith('G1'):
            
            for command in line.split():
                if command.startswith('X'):
                    x = float(command[1:])
                elif command.startswith('Y'):
                    y = float(command[1:])
                elif command.startswith('Z'):
                    try:
                        z = float(command[1:])
                    except:
                        er = True
            coordinates.append([x, y, z])

# Convert the list to a numpy array and transpose it
coordinates = np.array(coordinates).T

# Create a 3D plot
# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(*coordinates)
ax.set_title('')

# Create a new Tkinter window
window = tk.Tk()
window.title("SonoBone Print Preview")

# Create a canvas and add the plot to it
canvas = FigureCanvasTkAgg(fig, master=window)
canvas.draw()
canvas.get_tk_widget().pack()

# Start the Tkinter event loop
tk.mainloop()