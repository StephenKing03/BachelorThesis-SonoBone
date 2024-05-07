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
import os


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
                x = float(values[0])
                y = float(values[1])
                z = float(values[2])
                a = float(values[3])
                b = float(values[4])
                c = float(values[5])
                e = 0
                #classic cartesian coordinates + three quaternion values
                pose = [x, y, z, a, b, c]
                cartesian_coordinates.append([pose[0], pose[1], pose[2], pose[3], pose[4], pose[5], e, False])
            else:
                er = True
                cartesian_coordinates.append([0, 0, 0, 0, 180, 0, -180, er])

            

            #---finished reading all the lines---

        coordinates = []
        #shift them into the middle and transform then into the rotating base system
        x_offset, y_offset = shift_to_middle(coordinates)
        for i in range(len(coordinates)):
            
            #shift to be centered
            cartesian_coordinates[i][0] += x_offset
            cartesian_coordinates[i][1] += y_offset
            #transform into rotating base
            pose = transform_rotating_base(cartesian_coordinates[i])	
            coordinates.append([pose[0:5], cartesian_coordinates[i][6], cartesian_coordinates[i][7]]) #transformed pose + extrusion values + error flag

    GlobalState().cartesian_coordinates = coordinates   
    GlobalState().coordinates = coordinates
    return coordinates

def display_preview():
    coordinates = np.array(GlobalState().cartesian_coordinates).T
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(*coordinates)
    filename = os.path.basename(GlobalState().filepath)
    ax.set_title(filename)

    #add printbed 
    circle = plt.Circle((0, 0), 5, color='black', fill=False)
    ax.add_artist(circle)

    # Create a new Tkinter window
    window = tk.Tk()
    window.title("SonoBone Print Preview")

    # Create a canvas and add the plot to it
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack()

#---write the coordinates (2D print) to the robot ---------------------------------------------------------
def write_coordinates(coordinates, self):


    self.SendCustomCommand(f'SetJointVelLimit({GlobalState().printspeed_modifier * RobotStats().joint_vel_limit/100/2})')
    uf.adjust_speed(GlobalState().printspeed_modifier, self)

    #coordinates consist of [x, y, z, e, er]        
    z_0 = RobotStats().min_z 
    i = 0
    length = len(coordinates)

    last_theta = 0

    #main printing loop
    for x, y, z, phi, theta, e, er in coordinates:

    #--------------------------loop control-----------------------------------------
        #wait in this position when the print is paused
        while(GlobalState().printing_state != 2): #print paused 
            if GlobalState().printing_state == 5:
                print("exit path 1")
                print(GlobalState().printing_state)
                return
            time.sleep(0.1)
        
        # Check printing_state if the print is stoppedc
            if GlobalState().printing_state == 5:  
                print("exit path 2")
                print(GlobalState().printing_state)
                return
    #-------------------------------------------------------------------------------
    #--------------------------progress report--------------------------------------
        i += 1 #index
        GlobalState().current_line = i
        GlobalState().current_progress = round(float(i)/float(length) * 100, 1)


    #-------------------------------------------------------------------------------
    #--------------------------checkpoint system------------------------------------
        #---Set Checkpoint---
        next_checkpoint = GlobalState().msb.SetCheckpoint(i)
        next_checkpoint_theta = theta

        if(i > 1):
            checkpoint.wait(timeout=5/GlobalState().printspeed_modifier * 100)
            start_time = time.time()
            print(f'Checkpoint {i} reached')
            sc.wait_base(checkpoint_theta, i-1)
            print(f'Checkpoint_theta {i} reached after {time.time() - start_time} seconds')
        checkpoint = next_checkpoint
        checkpoint_theta = next_checkpoint_theta
        
    #-------------------------------------------------------------------------------
    #--------------------------send print commands----------------------------------
        uf.commandPose5d(x+RobotStats().center_x, y + RobotStats().center_y, z + RobotStats().min_z + GlobalState().user_z_offset, a, 0, -180, self)
        sc.turn_base(theta, i)
        GlobalState().last_pose = [x+x_offset, y + y_offset, z + z_0 + 10 + GlobalState().user_z_offset, phi, 0, -180]
        GlobalState().last_base_angle = theta
        print(f'Printing line {i} of {length} at {GlobalState().current_progress}%')
        if(e != None ):
                #sc.send_position(e - last_e)
                last_e = e

        time.sleep(0.01)
        GlobalState().checkpoint_reached = False
        
        #-------------------finished print -----------------------------
    

    #sc.send_speed(0)
    #set speed higher again
    GlobalState().msb.SendCustomCommand(f'SetJointVelLimit({RobotStats().start_joint_vel_limit})')
    uf.endpose(self)
    #print finished
    GlobalState().printing_state = 4
    return

#main printing function - refers to the other functions in this file
def start_print():
    
    #Extract coordinates
    GlobalState().terminal_text += "Extracting coordinates from file..."
    coordinates = extract_coordinates(GlobalState().filepath)
    
    for i in range(len(coordinates)):
        if uf.check_round_bounds(coordinates[i][0], coordinates[i][1]):

            GlobalState().terminal_text += "Select a different File that fits"
            GlobalState().occupied = False
            GlobalState().printing_state = 5
        return
        
    
    time.sleep(2)
    GlobalState().terminal_text += " --done! - Starting print--"
    
    #wait for msb != None with timeout
    start_time = time.time() #reset timer
    timeout = False
    while (GlobalState().msb == None and timeout):
        if(time.time() - start_time > 10):
            timeout = True
            break
        time.sleep(0.1)

    if timeout == True:
        GlobalState().terminal_text += "Robot not connected"
        GlobalState().occupied = False
        GlobalState().printing_state = 5
        return

    time.sleep(1)
    
    #set starting position
    uf.startpose(GlobalState().msb)
    GlobalState().msb.WaitIdle()

    #start printing
    GlobalState().printing_state = 2
    write_coordinates(coordinates,GlobalState().msb)

    return

'''coordinate transformation functions'''
def rad_to_deg(rad):
    return rad * 180 / np.pi

def rotation_around_z(pre, theta):
    return np.array([[np.cos(theta), -np.sin(theta), 0],
                     [np.sin(theta), np.cos(theta), 0],
                     [0, 0, 1]]) @ pre 

def transform_rotating_base(coordinate):

    r = coordinate[3:6]
    p_pre = coordinate[0:3]
    #print("r: " + str(r))
    #print("p: " + str(p_pre))

    #get angle phi from v to z-axis
    phi = np.arccos(r[2] / np.linalg.norm(r))

    #get angle theta from v projected into the xy-plane to y-axis
    theta = np.arccos(r[1] / (np.sin(phi) * np.linalg.norm(r)))


    #transform coordinates from before p_pre to p_post
    p_post = rotation_around_z(p_pre, theta)

    
    return [p_post[0], p_post[1], p_post[2], rad_to_deg(theta), rad_to_deg(phi), 0]


def shift_to_middle(coordinates):

    min_x = coordinates[0][0]
    max_x = coordinates[0][0]
    max_y = coordinates[0][1]
    min_y = coordinates[0][1]
    min_z = 0
    max_z = 0

    #get max and min x and y
    for x, y, z, a, b, c, e, er in coordinates:
        if x != None:
            if x > max_x:
                max_x = x
            elif x < min_x:
                min_x = x
        if y != None:
            if y > max_y:
                max_y = y
            elif y < min_y:
                min_y = y
        

        GlobalState().max_z_offset = RobotStats().max_z - max_z


#calculate offset so that the print is centered
    '''           + (half the distance left if evenly spaced)     '''
    x_offset = -min_x  + (max_x - min_x) /2
    '''         (align to the left edge)      + (half the distance left if evenly spaced)      '''
    y_offset = -min_y  + max_y - min_y /2


    return x_offset, y_offset