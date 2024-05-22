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
#---extract the coordinates from the gcode file---------------------------------------------------------
def extract_coordinates(file_path):
    coordinates = []

    
    with open(file_path, 'r') as file:
        i = 0
        x = 0
        y = 0
        z = 0
        
        e = 0
        
        for line in file:
            print(line)
            if i <44:
                i+=1
                continue
            #if line.startswith(';TIME_ELAPSED'):
                #break
            if line.startswith('G0') or line.startswith('G1'):
                
                er = False
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
                    elif command.startswith('E'):
                        e = float(command[1:])
                coordinates.append([x, y, z, e, er])
                
    GlobalState().cartesian_coordinates = coordinates
    return coordinates

def display_preview():
    coordinates = np.array(GlobalState().cartesian_coordinates).T
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(*coordinates)
    filename = os.path.basename(GlobalState().filepath)
    ax.set_title(filename)

    #add printbed 
    #circle = plt.Circle((0, 0), 5, color='black', fill=False)
    #ax.add_artist(circle)

    # Create a new Tkinter window
    window = tk.Tk()
    window.title("SonoBone Print Preview")

    # Create a canvas and add the plot to it
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack()

#---write the coordinates (2D print) to the robot ---------------------------------------------------------
def write_coordinates(coordinates,x_offset, y_offset, self):


    self.SendCustomCommand(f'SetJointVelLimit({GlobalState().printspeed_modifier * RobotStats().joint_vel_limit/100/2})')
    uf.adjust_speed(GlobalState().printspeed_modifier, self)

    #coordinates consist of [x, y, z, e, er]        
    z_0 = RobotStats().min_z 
    i = 0
    length = len(coordinates)

    last_theta = 0

    #main printing loop
    sc.extrude_speed()
    for x, y, z, e, er in coordinates:

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

        if(i > 1):
            checkpoint.wait(timeout=5/GlobalState().printspeed_modifier * 100)
            start_time = time.time()
            #print(f'Checkpoint {i} reached')
            
            print(f'Checkpoint_theta {i} reached {time.time() - start_time} seconds after robot arm reached')
        checkpoint = next_checkpoint
        
    #-------------------------------------------------------------------------------
    #--------------------------send print commands----------------------------------
        uf.commandPose(x+x_offset, y + y_offset, z + RobotStats().min_z + GlobalState().user_z_offset, 180, 0, -180, self)
        #sc.turn_base(theta, i)
        GlobalState().last_pose = [x, y, z + z_0  + GlobalState().user_z_offset, 180, 0, -180]
        print(f'Printing line {i} of {length} at {GlobalState().current_progress}%')
        #sc.send_position(e - last_e)
        last_e = e

        time.sleep(0.01)
        GlobalState().checkpoint_reached = False
        
        #-------------------finished print -----------------------------
    
    sc.stop_extrude
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
            
    x_offset,y_offset = modify_placement(coordinates)
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
    write_coordinates(coordinates, x_offset, y_offset,GlobalState().msb)

    return

def modify_placement(coordinates):

    min_x = coordinates[0][0]
    max_x = coordinates[0][0]
    max_y = coordinates[0][1]
    min_y = coordinates[0][1]
    min_z = 0
    max_z = 0

    #get max and min x and y
    for x, y, z, e, er in coordinates:
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
        if z != None:
            if z > RobotStats().max_z:
                max_z = z
            elif z < RobotStats().min_z:
                min_z = z

        GlobalState().max_z_offset = RobotStats().max_z - max_z

    #check if dimensions are feasible
    if (max_x - min_x) > (RobotStats().max_x - RobotStats().min_x):
        print("X-dimension too large")
        GlobalState().terminal_text += "\nX-dimensions are too large for the printebed for Δx = " + str(max_x-min_x)+ " \n" + "It must be within Δx = " + str(RobotStats().max_x - RobotStats().min_x)
        time.sleep(2)
        return None, None
    if (max_y - min_y) > (RobotStats().max_y - RobotStats().min_y):
        print("Y-dimension too large")
        GlobalState().terminal_text += "\nY-dimension are too large for the printebed for Δy = " + str(max_y-min_y)+ " \n" + "It must be within Δy = " + str(RobotStats().max_y - RobotStats().min_y) 
        time.sleep(2)
        return None, None

    
        
    
    
    #calculate offset so that the print is centered
    '''         (align to the lower edge)      + (half the distance left if evenly spaced)     '''
    x_offset = (-min_x + RobotStats().min_x) + ((RobotStats().max_x - RobotStats().min_x) - (max_x - min_x)) /2
    '''         (align to the left edge)      + (half the distance left if evenly spaced)      '''
    y_offset = (-min_y + RobotStats().min_y) + ((RobotStats().max_y - RobotStats().min_y) - (max_y - min_y )) /2


    return x_offset, y_offset