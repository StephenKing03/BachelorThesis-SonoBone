import numpy as np
import matplotlib.pyplot as plt
from tkinter import filedialog
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D


#---extract the coordinates from the gcode file---------------------------------------------------------
def extract_coordinates(file_path):
    cartesian_coordinates = []

    
    with open(file_path, 'r') as file:

        i = 0
        x = 0
        y = 0
        z = 0
        a = 0
        b = 0
        c = 0
        e = 0
        
        for line in file:
            
            er = False
            values = line.split()
            if len(values) >= 6:
                x = 0.1*float(values[0])
                y = 0.1*float(values[1])
                z = 0.1*float(values[2])
                a = float(values[3])
                b = float(values[4])
                c = float(values[5])
                e = 0
                #classic cartesian coordinates + three quaternion values
                pose = [x, y, z, a, b, c]
                #print(pose)
                
                cartesian_coordinates.append([pose[0], pose[1], pose[2], pose[3], pose[4], pose[5], e, False])
            else:
                er = True
                cartesian_coordinates.append([0, 0, 0, 0, 180, 0, -180, er])


    return cartesian_coordinates

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

def visualize_coordinates():
    # Get the coordinates
    file_path = filedialog.askopenfilename()
    coordinates = extract_coordinates(file_path)  # Replace this with the function that returns your coordinates

    # Convert the list to a numpy array and transpose it
    coordinates = np.array(coordinates).T

    # Create a 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Set the labels for the axes
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # Check the shape of the coordinates array
    if coordinates.shape[0] >= 3:
        # If there are three or more sets of values, plot the first three as x, y, z
        ax.plot(coordinates[0][0:10], coordinates[1][0:10], coordinates[2][0:10])
    else:
        raise ValueError("Invalid number of coordinate sets")

    plt.show()

visualize_coordinates()
