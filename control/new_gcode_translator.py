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
    coordinates = []

    with open(file_path, 'r') as file:

        start = False #start variable to get rid of header
        i = 0
        x = None
        y = None
        z = None
        a = 180
        b = 0
        c = -180
        f = 0
        e = 0
        
        min_x = None
        max_x = None
        min_y = None
        max_y = None
        min_z = None
        max_z = None
        
        #iterate over all the lines of the text/gcode file
        for line in file:
            if line.startswith(';LAYER:0'):
                start = True #start signal

            if line.startswith('G91 ;Relative positioning'):
                break #end signal

            if start == True and (line.startswith('G0') or line.startswith('G1')):
                for command in line.split():
                    #if there is an x-value
                    if command.startswith('X'):
                        #enter the x_value into the command
                        x = float(command[1:]) 

                        #update the min and max values of x for centering purposes
                        if min_x == None or x < min_x:
                            min_x = x
                        if max_x == None or x > max_x:
                            max_x = x

                    #if there is a y-value
                    elif command.startswith('Y'):
                        #enter the y_value into the command
                        y = float(command[1:])

                        #update the min and max values of y for centering purposes
                        if min_y == None or y < min_y:
                            min_y = y
                        if max_y == None or y > max_y:
                            max_y = y

                    #if there is a z-value
                    elif command.startswith('Z'):
                        try:
                            z = float(command[1:]) #reading of the z value can be buggy somehow
                            #update the min and max values of z for centering purposes
                            if min_z == None or z < min_z:
                                min_z = z
                            if max_z == None or z > max_z:
                                max_z = z
                        except:
                            time.sleep(0.01)

                    #extrusion and feeder values
                    elif command.startswith('E'):
                        e = float(command[1:])
                    elif command.startswith('F'):
                        f = float(command[1:])
                        
                    #current standby for euler angle positions
                    a = 180
                    b = 0
                    c = -180

                    if(x != None and y != None and z != None):
                        #print(x, y, z, a, b, c, e, f)
                        coordinates.append([x, y, z, a, b, c, e, f])   

        #check maximum size of the print
        if(max_x-max_y > RobotStats().max_x- RobotStats().min_x):
            GlobalState().terminal_text +=("Print too large in x-direction for delta x = " + str(max_x - min_x) + "it must be withing the range of delta x = " + str(RobotStats().max_x - RobotStats().min_x))
            return
        if(max_y-min_y > RobotStats().max_y- RobotStats().min_y):
            GlobalState().terminal_text+=("Print too large in y-direction for delta y = " + str(max_y - min_y) + "it must be withing the range of delta y = " + str(RobotStats().max_y - RobotStats().min_y))
            return
        if(max_z-min_z > RobotStats().max_z- RobotStats().min_z):
            GlobalState().terminal_text +=("Print too large in z-direction for delta z = " + str(max_z - min_z) + "it must be withing the range of delta z = " + str(RobotStats().max_z - RobotStats().min_z))
            return False
            
        #-finished iterating over all the lines in the code 
        x_offset = -min_x - (max_x - min_x) /2
        y_offset = -min_y - (max_y - min_y) /2
        z_offset = -min_z

        centered_coordinates = []
        for x,y,z,a,b,c,e,f in coordinates:

            centered_coordinates.append([x+x_offset, y+y_offset, z+z_offset, a, b, c, e, f])  
        
        
        #modify the coordinates so that they are centered  
        printing_coordinates = modify_coordinates(coordinates, x_offset,y_offset,z_offset)
    
        GlobalState().coordinates = printing_coordinates
        GlobalState().cartesian_coordinates = centered_coordinates          

def modify_coordinates(cartesian_coordinates, x_offset, y_offset, z_offset):

    printing_coordinates = []
    
    for x,y,z,a,b,c,e,f in cartesian_coordinates:

        printing_coordinates.append([x+x_offset, y+y_offset, z+z_offset, a, b, c, e, f])   

    return printing_coordinates


def write_coordinates():

    coordinates = GlobalState().coordinates
    #get robot object
    msb = GlobalState().msb

    #loop iteration index
    i = 0
    j = 0
    extruder_zero = 0.5
   
    
    #set speed to printing speed
    msb.SendCustomCommand(f'SetJointVelLimit({GlobalState().printspeed_modifier * RobotStats().joint_vel_limit/100/2})')
    uf.adjust_speed(GlobalState().printspeed_modifier, msb)
    #sc.send_combined_position(0, 10, 1, 1)
    #GlobalState.arduino_info.clear()
    sc.start_reset()
    '''
    #initial setup
    sc.reset_pos(0)
    theta_base = 0
    '''

    time.sleep(1)
    #**main printing loop**
    for x,y,z,a,b,c,e,f in coordinates:

        #override for planar printing
        a = 180
        theta_base = 0

        #theoretical calculating of the base position

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

        #--------------------------progress report--------------------------------------
        i += 1 #index
        if j < 100:
            j += 1 #index
        else:
            j = 1 #checkpoint system only goes to max of 8000 on the robot =(
            GlobalState().arduino_info.clear()

        GlobalState().current_line = i
        GlobalState().current_progress = round(float(i)/float(len(coordinates)) * 100, 1)

        #--------------------------checkpoint system------------------------------------
        
        #create checkpoint for the program to wait so that the poses are synchronized
        if(i %4 == 0):
            next_checkpoint = GlobalState().msb.SetCheckpoint(j)
        
        #wait for arduino to confirm success:
        timeout_time = time.time()
        if(i>9 and i % 4 == 0):
            while sc.done_arduino_queue(i-3) == False:
                if(time.time() - timeout_time > 0.2):
                    print("TIMEOUT ERROR")
                    break

                if GlobalState().printing_state != 2:  
                    print("exit path 4")
                    print(GlobalState().printing_state)
                    break
                time.sleep(0.1)

        #wait for robot arm to have reached the position
        if(i > 9 and i % 4 == 0):
            checkpoint.wait(timeout=5/GlobalState().printspeed_modifier * 100)

        #move checkpoint object for the next iteration
        if i%4 == 0 and i > 4:
            checkpoint = next_checkpoint

        distance = (((GlobalState().last_pose[0]-x)**2 + (GlobalState().last_pose[1]-y)**2 + (GlobalState().last_pose[2]-z)**2) **0.5)

        #-----------------------send commands--------------------------------------------
        uf.commandPose(x+RobotStats().center_x,y+RobotStats().center_y,z+RobotStats().min_z+GlobalState().user_z_offset,a,0,-180)
        if(i % 2 == 0):
            sc.send_combined_position(theta_base, e + extruder_zero, j, distance)
            GlobalState().last_pose = [x+RobotStats().center_x,y+RobotStats().center_y,z*1.3+RobotStats().min_z+GlobalState().user_z_offset,a,0,-180]


    #print loop finished

    #set speed higher again
    GlobalState().msb.SendCustomCommand(f'SetJointVelLimit({RobotStats().start_joint_vel_limit})')
    uf.endpose(msb)
    #print finished
    GlobalState().printing_state = 4
    return

def start_print():

    GlobalState().terminal_text += "Extracting coordinates from file..."
    if(extract_coordinates(GlobalState().filepath) == False):
        print("exit due to size")
        GlobalState().terminal_text += "please select a smaller print"
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
    write_coordinates()

    return


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
        ax.set_xlim(-40, 40)
        ax.set_ylim(-40, 40)
        ax.set_zlim(0, 100)



        # Check the shape of the coordinates array
        if coordinates.shape[0] >= 3:
            # If there are three or more sets of values, plot the first three as x, y, z
            ax.plot(coordinates[0][::5], coordinates[1][::5], coordinates[2][::5])
        else:
            raise ValueError("Invalid number of coordinate sets")
        
        # Add a circle in the z-plane
        circle = patches.Circle((0, 0, 0),30, color='r', fill=False)  # Create a circle at the origin with radius 50
        ax.add_patch(circle)  # Add the circle to the plot
        art3d.pathpatch_2d_to_3d(circle, z=0, zdir="z")  # Convert the 2D circle to a 3D patch at z=0
        
        plt.show()  
    else:
        GlobalState().terminal_text += "Visualization not possible \n - wait for coordinates to be extracted first"            

    return