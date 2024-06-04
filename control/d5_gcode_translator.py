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


#---extract the coordinates from the gcode file---------------------------------------------------------
def extract_coordinates(file_path):
    cartesian_coordinates = []

    
    with open(file_path, 'r') as file:

        i = 0
        
        
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

            if line.startswith('G0') or line.startswith('G1'):
                for command in line.split():
                    if command.startswith('X'):
                        x = float(command[1:])
                    elif command.startswith('Y'):
                        y = float(command[1:])
                    elif command.startswith('Z'):
                        z = float(command[1:])
                    elif command.startswith('A'):
                        a = float(command[1:])
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
                        #classic cartesian coordinates + three quaternion values                      
                        cartesian_coordinates.append([x, y, z, a, b, c, e, f])
                        e = 1
                    
            #---finished reading all the lines---

        coordinates = []
        #shift them into the middle and transform then into the rotating base system
        x_offset, y_offset, z_offset = shift_to_middle(cartesian_coordinates)
        #print("x_offset: " + str(x_offset) + " y_offset: " + str(y_offset))
        for i in range(len(cartesian_coordinates)):
            
            #shift to be centered
            cartesian_coordinates[i][0] += x_offset
            cartesian_coordinates[i][1] += y_offset
            cartesian_coordinates[i][2] += z_offset
            #transform into rotating base
            pose = transform_rotating_base(cartesian_coordinates[i])
            coordinates.append([pose[0], pose[1], pose[2], pose[3], pose[4], cartesian_coordinates[i][6], cartesian_coordinates[i][7]]) #transformed pose + extrusion values + error flag

    GlobalState().cartesian_coordinates = cartesian_coordinates   
    GlobalState().coordinates = coordinates

    #print(coordinates)

    return coordinates



import matplotlib.patches as patches
from mpl_toolkits.mplot3d import art3d

def display_preview():
    # Get the coordinates
    if(GlobalState().cartesian_coordinates != []):
        coordinates = GlobalState().cartesian_coordinates
        

        # Convert the list to a numpy array and transpose it
        coordinates = np.array(coordinates).T
        print(coordinates)
        # Create a 3D plot
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Set the labels for the axes
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        '''
        ax.set_xlim(-1, 1)
        ax.set_ylim(-1, 1)
        ax.set_zlim(0, 2)
        '''

            # Check the shape of the coordinates array
        if coordinates.shape[0] >= 3:
            # If there are three or more sets of values, plot the first three as x, y, z
            ax.plot(coordinates[0][0:10], coordinates[1][0:10], coordinates[2][0:10])
        else:
            raise ValueError("Invalid number of coordinate sets")
        
        # Add a circle in the z-plane
        circle = patches.Circle((0, 0, 0),0.005, color='r', fill=False)  # Create a circle at the origin with radius 50
        ax.add_patch(circle)  # Add the circle to the plot
        art3d.pathpatch_2d_to_3d(circle, z=0, zdir="z")  # Convert the 2D circle to a 3D patch at z=0
        
        plt.show()  
    else:
        GlobalState().terminal_text += "Visualization not possible \n - wait for coordinates to be extracted first"            

    return
#---write the coordinates (2D print) to the robot ---------------------------------------------------------
def write_coordinates(coordinates, self):


    self.SendCustomCommand(f'SetJointVelLimit({GlobalState().printspeed_modifier * RobotStats().joint_vel_limit/100/2})')
    uf.adjust_speed(GlobalState().printspeed_modifier, self)

    #coordinates consist of [x, y, z, e, er]        
    z_0 = RobotStats().min_z 
    i = 0
    length = len(coordinates)

    #main printing loop
    for x, y, z, phi_robot, theta_base, e, f in coordinates:

    #--------------------------loop print control-----------------------------------------
        #wait in this position when the print is paused
        while(GlobalState().printing_state != 2): #print paused 
            if GlobalState().printing_state == 5:
                print("exit path 1")
                print(GlobalState().printing_state)
                return
            time.sleep(0.1)
        
        # Check printing_state if the print is stopped
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
        next_checkpoint_theta_base = theta_base
        
        #wait for base to be reached
        if(i>1):
            #print("wait done base: " + str(i-1))
            while sc.done_base(i-1) == False:
                if GlobalState().printing_state != 2:  
                    print("exit path 4")
                    print(GlobalState().printing_state)
                    break
                time.sleep(0.1)
            
        
        #make it that the first position is already there
        #if(i == 1):
            #sc.reset_pos(theta_base)
        
        if(i > 1):
            checkpoint.wait(timeout=5/GlobalState().printspeed_modifier * 100)
            start_time = time.time()
            #print(f'Checkpoint {i} reached')
            #sc.wait_done_base(checkpoint_theta_base, i-1)
            print(f'Checkpoint_theta_base {i} reached {time.time() - start_time} seconds after robot arm reached')
        checkpoint = next_checkpoint
        checkpoint_theta_base = next_checkpoint_theta_base
        
    #-------------------------------------------------------------------------------
    #--------------------------send print commands----------------------------------

        if(phi_robot < 130 and phi_robot > 0):
            phi_robot = 130
            print("corrected")
        elif (phi_robot > -130 and phi_robot < 0):
            phi_robot = 230
            print("corrected")
        
        uf.commandPose5d(x+RobotStats().center_x, y + RobotStats().center_y, z + RobotStats().min_z + GlobalState().user_z_offset, phi_robot, 0, -180, self)
        if e == 0:
            sc.stop_extrude()
            sc.send_base_solo_position(theta_base, i)
            print("Sent solo position: " + str(i))
        else:
            sc.send_combined_position(theta_base, i)
            print("Sent combined position: " + str(i))
        GlobalState().last_pose = [x, y, z + z_0  + GlobalState().user_z_offset, phi_robot, 0, -180]
        GlobalState().last_base_angle = theta_base
        print(f'Printing line {i} of {length} at {GlobalState().current_progress}%')
        

        time.sleep(0.01)
        GlobalState().checkpoint_reached = False
        
        #-------------------finished print -----------------------------
    

    #set speed higher again
    GlobalState().msb.SendCustomCommand(f'SetJointVelLimit({RobotStats().start_joint_vel_limit})')
    uf.endpose(self)
    sc.stop_extrude()
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

def rotation_around_z(pre, theta_base):
    return np.array([[np.cos(theta_base), -np.sin(theta_base), 0],
                     [np.sin(theta_base), np.cos(theta_base), 0],
                     [0, 0, 1]]) @ pre 

def transform_rotating_base(coordinate):

    r = coordinate[3:6]
    p_pre = coordinate[0:3]
    #print("r: " + str(r))
    #print("p: " + str(p_pre))

    #get angle phi_robot from v to z-axis
    phi_robot = np.arccos(r[2] / np.linalg.norm(r))

    #get angle theta_base from v projected into the xy-plane to y-axis
    theta_base = np.arccos(r[1] / (np.sin(phi_robot) * np.linalg.norm(r)))


    #transform coordinates from before p_pre to p_post
    p_post = rotation_around_z(p_pre, theta_base)

    
    return [p_post[0], p_post[1], p_post[2], rad_to_deg(theta_base), rad_to_deg(phi_robot), 0]


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
        if z != None:
            if z > max_z:
                max_z = z
            elif z < min_z:
                min_z = z
        

        GlobalState().max_z_offset = RobotStats().max_z - max_z


#calculate offset so that the print is centered
    x_offset = -min_x - (max_x - min_x) /2
    y_offset = -min_y - (max_y - min_y) /2
    z_offset = -min_z


    return x_offset, y_offset, z_offset