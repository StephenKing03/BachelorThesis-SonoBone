import numpy as np
import matplotlib.pyplot as plt
from tkinter import filedialog
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D
import math
import time #for time.sleep()
import utility_functions as uf #import utility functions
import stepper_control as sc
from globals import GlobalState
from globals import RobotStats


import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.patches as patches
from mpl_toolkits.mplot3d import art3d
import os



def extract_coordinates(file_path):
    cartesian_coordinates = []

    
    with open(file_path, 'r') as file:

        i = 0
        last_a = 0
        g92_a = 0
        g92_y = 0
        g92_z = 0
        last_y = 0
        last_z = 0
        
        
        for line in file:

            x = None
            y = None
            z = None
            a = None
            b = None
            c = None
            f = None
            e = 1
            
            

            #skip the first 17 lines
            if i <17:
                i+=1
                continue

            if line.startswith('G92'):
                g92_a += last_a
                g92_y += last_y
                g92_z += last_z
                #print("G92")
                continue
            elif line.startswith('G0') or line.startswith('G1'):
                for command in line.split():
                    if command.startswith('X'):
                        x = float(command[1:])
                    elif command.startswith('Y'):
                        y = float(command[1:])
                        last_y = y
                    elif command.startswith('Z'):
                        z = float(command[1:])
                        last_z = z
                    elif command.startswith('A'):
                        a = float(command[1:])
                        last_a = a
                    elif command.startswith('B'):
                        b = float(command[1:])
                    elif command.startswith('C'):
                        c = float(command[1:])
                    elif command.startswith('E'):
                        e = float(command[1:])
                    elif command.startswith('F'):
                        f = float(command[1:])
                        
                    
                    if x == None or y == None or z == None or a == None or b == None or c == None or f == None:
                        e = 0
                        continue

                    else:
                        
                        #x = x * math.cos(math.radians(g92_a))
                        y =   y + (y-last_y) * math.cos(math.radians(g92_a)) + (z-last_z) * math.sin(math.radians(g92_a))
                        z =  z+ (z-last_z) * math.cos(math.radians(g92_a)) - (y-last_y) * math.sin(math.radians(g92_a))

                        #classic cartesian coordinates + three quaternion values                      
                        cartesian_coordinates.append([x, y, z, a, b, c, e, f])
                        e = 1
    return cartesian_coordinates


from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
def display_preview():
    # Get the coordinates
    
        file_path = filedialog.askopenfilename()
        coordinates = extract_coordinates(file_path)

        # Convert the list to a numpy array and transpose it
        coordinates = np.array(coordinates).T

        # Create a 3D plot
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Set the labels for the axes
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        #ax.set_xlim(-100, 100)
        #ax.set_ylim(-100, 100)
        #ax.set_zlim(0, 200)


            # Check the shape of the coordinates array
        if coordinates.shape[0] >= 3:
            # If there are three or more sets of values, plot the first three as x, y, z
            #ax.plot(coordinates[0][0:2000], coordinates[1][0:2000], coordinates[2][0:2000])
            ax.scatter(coordinates[0], coordinates[1], coordinates[2])
        else:
            raise ValueError("Invalid number of coordinate sets")

        # Add a circle in the z-plane
        circle = patches.Circle((0, 0),50, color='r', fill=False)  # Create a circle at the origin with radius 50
        ax.add_patch(circle)  # Add the circle to the plot
        art3d.pathpatch_2d_to_3d(circle, z=0, zdir="z")  # Convert the 2D circle to a 3D patch at z=0

        plt.show()  
    

display_preview()
