import customtkinter as ctk
import tkinter as tk
import string
import os
import threading
import time
from datetime import datetime
import mecademicpy.robot as mdr
from PIL import Image, ImageTk
import sys

from tkinter import filedialog

import utility_functions as uf  # import utility functions
import gcode_translator as gt  # import gcode translator
import stepper_control as sc  # import stepper control
import d5_gcode_translator as d5 #5d test file

from globals import GlobalState
from globals import RobotStats

def button_function():
    print("Button pressed")
    return

global status_text
global z_offset_textbox
global speed_textbox
global terminal_text
global pause_button
global e_speed_textbox
global progress_text
global calibrate_button
global file_button
global stop_button
global init_button
global start_button
global z_offset_up_button
global z_offset_down_button
global speed_up_button
global speed_down_button
global e_speed_up_button
global e_speed_down_button
global calibrate_button
global reset_button




def print_control(root, leftcol, rightcol, buttoncolor, rcol):
    #button to initialize the robot
    global init_button
    init_button = ctk.CTkButton(master=root, text="Initialize Robot", font=("Avenir Heavy",15), fg_color= buttoncolor, command=init_print_but)
    init_button.place(relx=leftcol, rely=0.35, anchor=ctk.NW)

    #button to set file path
    global file_button
    file_button = ctk.CTkButton(master=root, text="Select File", font=("Avenir Heavy",15),fg_color= '#089DC3', command=select_file_but)
    file_button.place(relx=leftcol, rely=0.45, anchor=ctk.NW)

    #button to start printing
    global start_button
    start_button = ctk.CTkButton(master=root, text="Start Printing", font=("Avenir Heavy",15),fg_color= buttoncolor, command=start_print_but)
    start_button.place(relx=leftcol, rely=0.55, anchor=ctk.NW)

    #button to stop printing
    global stop_button
    stop_button = ctk.CTkButton(master=root, text="Stop Printing", font=("Avenir Heavy",15), fg_color= '#DC0F24' ,command=stop_print_but)
    stop_button.place(relx=leftcol, rely=0.75, anchor=ctk.NW)

    #button to pause and resume printing
    global pause_button
    pause_button = ctk.CTkButton(master=root, text="Pause Printing", font=("Avenir Heavy",15), fg_color= buttoncolor, command=pause_print_but)
    pause_button.place(relx=leftcol, rely=0.65, anchor=ctk.NW)

    #button to callibrate the robot
    global calibrate_button
    calibrate_button = ctk.CTkButton(master=root, text="Calibrate", font=("Avenir Heavy",15), fg_color= buttoncolor, command=calibration_but)
    calibrate_button.place(relx=leftcol, rely=0.9, anchor=ctk.NW)

    global reset_button
    reset_button = ctk.CTkButton(master=root, text="Reset", font=("Avenir Heavy",13), text_color = '#030303', width = 50, height = 25, fg_color= '#ECE331', command=reset_but)
    reset_button.place(relx=rcol +0.08, rely=0.25, anchor=ctk.NW)

    return

def print_monitor(root, leftcol, rightcol, buttoncolor, rcol):

    global status_text
    global terminal_text
    

    #status infos
    status_label = ctk.CTkLabel(master=root, text="Status:", font=("Avenir Heavy", 15, 'bold'), width = 40, pady = 10, anchor = 'center')
    status_label.place(relx=leftcol, rely=0.18, anchor=ctk.NW)

    status_text = ctk.CTkLabel(master=root, text = " - ", font=("Avenir Heavy",12), height=4, width=450, anchor = ctk.W)
    status_text.place(relx=leftcol, rely=0.25, anchor=ctk.NW)

    status_update("Deactivated")

    #terminal info
    terminal_label = ctk.CTkLabel(master=root, text="Print info", font=("Avenir Heavy", 15, 'bold'), width = 40, pady = 10, anchor = 'center')
    terminal_label.place(relx=rightcol, rely=0.18, anchor=ctk.NW)

    terminal_text = tk.Text(master=root, font=("Avenir",12), height=26, width=57, bg = '#1A0F10', fg = '#FFFFFF')
    terminal_text.place(relx=rightcol, rely=0.25, anchor=ctk.NW)

    scrollbar = tk.Scrollbar(root, command=terminal_text.yview, background = 'blue')
    scrollbar.place(relx=rightcol+0.43, rely=0.25, anchor=ctk.NW, height=root.winfo_screenheight()*0.59)
    terminal_text['yscrollcommand'] = scrollbar.set

    terminal_text.insert(ctk.END, "")

    return

def cosmetics(root, leftcol, rightcol, buttoncolor, rcol):

    #title
    info_title = ctk.CTkLabel(master=root, text="SonoBone control interface", font=("Avenir Heavy", 31, 'bold'), fg_color= '#333332', width = root.winfo_screenwidth(), pady = 5, anchor = 'center')
    info_title.place(relwidth = 1)

    #cool icon
    image = Image.open(search_file("cool_robot_icon.png"))
    image  = image.resize((70,70))
    photo = ImageTk.PhotoImage(image)
    icon_label = ctk.CTkLabel(master=root, image=photo,fg_color= '#333332', text = "")
    icon_label.place(relx=0.12, rely=0.015, anchor=ctk.NW)

    return

def tuning(root, leftcol, rightcol, buttoncolor, rcol):

    global z_offset_textbox
    global speed_textbox
    global e_speed_textbox

    global z_offset_up_button
    global z_offset_down_button
    global speed_up_button
    global speed_down_button
    global e_speed_up_button
    global e_speed_down_button

    #set z offsetbutton up and down
    z_offset_up_button = ctk.CTkButton(master=root, text="↑", font=("Avenir Heavy",15), fg_color= buttoncolor, command=z_up_but, width = 50, height = 25, anchor = 'center')
    z_offset_up_button.place(relx=rcol, rely=0.25, anchor=ctk.NW)
    z_offset_down_button = ctk.CTkButton(master=root, text="↓", font=("Avenir Heavy",15), fg_color= buttoncolor, command=z_down_but, width = 50, height = 25, anchor = 'center')
    z_offset_down_button.place(relx=rcol, rely=0.45, anchor=ctk.NW)

    #z offset textbox
    z_offset_textbox = ctk.CTkEntry(master=root, font=("Avenir", 10), width=50)
    z_offset_textbox.place(relx=rcol, rely=0.35, anchor=ctk.NW)
    # Set the text of z_offset_textbox
    z_offset_textbox.insert(0, str(GlobalState().user_z_offset) + "mm")

    z_offset_label= ctk.CTkLabel(master=root, text="Z-offset", font=("Avenir Heavy", 15, 'bold'), width = 40, anchor = 'center')
    z_offset_label.place(relx=rcol, rely=0.18, anchor=ctk.NW)

    #set speed button up and down
    speed_up_button = ctk.CTkButton(master=root, text="↑", font=("Avenir Heavy",15), fg_color= buttoncolor, command=speed_up_but, width = 50, height = 25)
    speed_up_button.place(relx=rcol, rely=0.63, anchor=ctk.NW)
    speed_down_button = ctk.CTkButton(master=root, text="↓", font=("Avenir Heavy",15), fg_color= buttoncolor, command=speed_down_but, width = 50, height = 25, anchor = 'center')
    speed_down_button.place(relx=rcol, rely=0.83, anchor=ctk.NW)

    #speed textbox
    speed_textbox = ctk.CTkEntry(master=root, font=("Avenir", 10), width=50)
    speed_textbox.place(relx=rcol, rely=0.73, anchor=ctk.NW)
    speed_textbox.insert(0, f'{GlobalState().printspeed_modifier}%')

    speed_label= ctk.CTkLabel(master=root, text="Speed", font=("Avenir Heavy", 15, 'bold'), width = 40, anchor = 'center')
    speed_label.place(relx=rcol, rely=0.56, anchor=ctk.NW)

    #set extrusion speed button up and down
    e_speed_up_button = ctk.CTkButton(master=root, text="↑", font=("Avenir Heavy",15), fg_color= buttoncolor, command=e_speed_up_but, width = 50, height = 25)
    e_speed_up_button.place(relx=rcol+0.08, rely=0.63, anchor=ctk.NW)
    e_speed_down_button = ctk.CTkButton(master=root, text="↓", font=("Avenir Heavy",15), fg_color= buttoncolor, command=e_speed_down_but, width = 50, height = 25, anchor = 'center')
    e_speed_down_button.place(relx=rcol+0.08, rely=0.83, anchor=ctk.NW)

    #extrusion speed textbox
    e_speed_textbox = ctk.CTkEntry(master=root, font=("Avenir", 10), width=50)
    e_speed_textbox.place(relx=rcol+0.08, rely=0.73, anchor=ctk.NW)
    e_speed_textbox.insert(0, f'{GlobalState().extrusion_speed_modifier}%')

    e_speed_label= ctk.CTkLabel(master=root, text="Extrusion", font=("Avenir Heavy", 15, 'bold'), width = 40, anchor = 'center')
    e_speed_label.place(relx=rcol+0.08, rely=0.56, anchor=ctk.NW)

    return

#------------------ Button functions ------------------

def start_print_but():

    global start_button
    start_button.configure(state="disabled")
    #if other button active don't do anything
    if GlobalState().confirmed == False:
        print("OCCUPIED")
        start_button.configure(state="normal")
        return
    GlobalState().confirmed = False
    

    if(GlobalState().printing_state != 1 and GlobalState().printing_state != 0):
        GlobalState().terminal_text += "Not ready for printing"
        GlobalState().confirmed = True
        start_button.configure(state="normal")
        return

    if(GlobalState().printing_state == 2 or GlobalState().printing_state == 3):
        GlobalState().terminal_text += "print already in progress - stop first"
        GlobalState().confirmed = True
        start_button.configure(state="normal")
        return

    #check if file path is set:
    if (GlobalState().filepath == " " or GlobalState().filepath == ''):
        GlobalState().terminal_text +="Error: No file selected"
        GlobalState().confirmed = True
        start_button.configure(state="normal")
        return 

    if(GlobalState().msb == None):
        GlobalState().terminal_text += "Error: Robot not initialized - initializing now..."
        GlobalState().confirmed = True
        init_print_but()

    GlobalState().confirmed = True

    GlobalState().current_progress = 0
    GlobalState().printing_state = 2 #2 = printing
    #start print
    filename = os.path.basename(GlobalState().filepath)
    status_update("Printing ...  \nFile: " + str(filename))

    progress_thread = threading.Thread(target=progress_update)
    progress_thread.start()

    ''' change this for the 5d print, exchange d5 with gt '''
    print_thread = threading.Thread(target=gt.start_print)  
    print_thread.start()
    
    #wait for program to finish to update the text
    finished_thread = threading.Thread(target=wait_for_printing)
    finished_thread.start()
    
    start_button.configure(state="normal")

    return


def wait_for_printing():
    while GlobalState().printing_state != 4:
        time.sleep(0.1)
    GlobalState().msb.WaitIdle()
    GlobalState().terminal_text += "-------------------PRINT FINISHED!-------------"
    uf.cleanpose(GlobalState().msb)
    time.sleep(3)
    
    status_update("Finished printing!\n  ready to print again")
    GlobalState.confirmd = True
    
    return

def stop_print_but():

    global stop_button
    stop_button.configure(state="disabled")
    
    if(GlobalState().confirmed == False):
        print("OCCUPIED")
        stop_button.configure(state="normal")
        return
    GlobalState().confirmed = False
    

    if(GlobalState().printing_state == 2):

        GlobalState().printing_state = 5 #5 = stopped
        GlobalState().msb.WaitIdle()
        GlobalState().confirmed = True
        GlobalState().terminal_text = " ---PRINT STOPPED---"
        status_update("Print stopped")

        stop_thread = threading.Thread(target=stop)
        stop_thread.start()

    else:
        GlobalState().terminal_text += "no print in process - nothing done"
        GlobalState().confirmed = True
        stop_button.configure(state="normal")
    
    
    #deactivate() optional to deactivate the robot
    return

def stop():
    global stop_button

    GlobalState().filepath = " "
    GlobalState().msb.ResetError()
    GlobalState().msb.SendCustomCommand(f'SetJointVelLimit({RobotStats().joint_vel_limit})')
    uf.cleanpose(GlobalState().msb)
    GlobalState().msb.WaitIdle()
    GlobalState().confirmed = True
    stop_button.configure(state="normal")
    GlobalState().printing_state = 1
    
    status_update("stopped - ready to print again")
    return

def init_print_but():

    global init_button
    init_button.configure(state="disabled")
    #if other button active don't do anything
    if GlobalState().confirmed == False:
        print("OCCUPIED")
        init_button.configure(state="")
        return
    GlobalState().confirmed = False
    

    if(GlobalState().msb != None):
        GlobalState().terminal_text += "Already Initialized"
        GlobalState().confirmed = True
        return
    GlobalState().terminal_text += "Initializing Robot..."

    
    #start the terminal thread
    terminal_thread = threading.Thread(target=terminal_update)
    terminal_thread.start()
   
    #set states and info text
    GlobalState().printing_state = 0 #0 = not printing

    init_thread = threading.Thread(target=init)
    init_thread.start()

    status_update("Ready to print")
    

    return

def init():

    global init_button

    uf.init_sequence()

    GlobalState().confirmed = True
    init_button.configure(state="normal")

    return

def select_file_but():

    global file_button
    file_button.configure(state="disabled")
    
    if(GlobalState().confirmed == False):
        print("OCCUPIED")
        file_button.configure(state="normal")
        return
    GlobalState().confirmed = False
    

    if(GlobalState().printing_state == 2 or GlobalState().printing_state == 3 ):
        GlobalState().terminal_text += "Please stop printing before selecting a new file!"
        file_button.configure(state="normal")
        return

    if(GlobalState().printing_state == 6):
        GlobalState().terminal_text += "Please stop calibration before selecting a new file!"
        file_button.configure(state="normal")
        return
    
    GlobalState().printing_state = 0 #0 = not printing
    #get the file path
    file_path = filedialog.askopenfilename()
    #print("Selected file:", file_path)

    if(file_path == ""):
        GlobalState().terminal_text += "No file selected"
        GlobalState().confirmed = True
        file_button.configure(state="normal")
        return

    # save the file path into GlobalState().filepath for later use
    GlobalState().filepath = file_path
    filename = os.path.basename(file_path)
    #status_update("File selected:\n'"  + filename + "'")
    
    GlobalState().terminal_text += f"File selected: '{filename}'"

    file_button.configure(state="normal")
    GlobalState().confirmed = True

    return

def pause_print_but():
    global pause_button

    pause_button.configure(state="disabled")
    if(GlobalState().confirmed == False):
        print("OCCUPIED")
        pause_button.configure(state="normal")
        return
    GlobalState().confirmed == False
   
    
    if(GlobalState().printing_state == 2):

        status_update("Printing paused")
        GlobalState().terminal_text = "---Printing paused---"

        pause_thread = threading.Thread(target=pause)
        pause_thread.start()
        
    elif(GlobalState().printing_state == 3):
        
        status_update("resuming print...")
        resume_thread = threading.Thread(target=resume)
        resume_thread.start()
    else:
        GlobalState().terminal_text += "no print in process - nothing done"

    return

def pause():    
    global pause_button
    
    #set cleanpose for adjustments
    #GlobalState().msb.WaitIdle()
    
    GlobalState().printing_state = 3 #3 = paused
    GlobalState().msb.SendCustomCommand(f'SetJointVelLimit({RobotStats().joint_vel_limit})')
    GlobalState().msb.WaitIdle()
    #GlobalState().msb.ClearMotion() #Watch OUT! This clears the motion queue
    time.sleep(0.3)
    uf.cleanpose(GlobalState().msb)
    GlobalState().msb.WaitIdle()
    GlobalState().confirmed = True
    pause_button.configure(state="normal")

    #set all states for pausing
    pause_button.configure(state="normal")
    pause_button.configure(text="Resume Printing")

    return

def resume():
    global pause_button
    #resume position
    #GlobalState().msb.WaitIdle()
    GlobalState().terminal_text += "resuming"
    uf.commandPose(GlobalState().last_pose[0], GlobalState().last_pose[1], GlobalState().last_pose[2], GlobalState().last_pose[3], GlobalState().last_pose[4], GlobalState().last_pose[5], GlobalState().msb)
    GlobalState().msb.WaitIdle()
    GlobalState().msb.SendCustomCommand(f'SetJointVelLimit({GlobalState().printspeed_modifier * RobotStats().joint_vel_limit/100/2})')
    #reset all states so that printing can continue
    GlobalState().confirmed = True
    pause_button.configure(state="normal")
    GlobalState().printing_state = 2 #2 = printing
    filename = os.path.basename(GlobalState().filepath)
    status_update("Printing ...  \nFile: " + str(filename))
    GlobalState().terminal_text += "---Printing resumed---"
    pause_button.configure(text="Pause Printing")
    return

def calibration_but():
    global calibrate_button
    calibrate_button.configure(state = "disabled")
    if(GlobalState().msb == None):
        GlobalState().terminal_text += "Error: Robot not initialized"
        calibrate_button.configure(state = "normal")
        return
    if(GlobalState().printing_state != 2 and GlobalState().printing_state != 3 and GlobalState().printing_state != 6):
        
        
        GlobalState().terminal_text += " ---Ready for callibration - 10mm above the bed--- "
        GlobalState().previous_state = GlobalState().printing_state
        GlobalState().printing_state = 6 #6 = calibration
        status_update("Calibrating...")

        #thread to update callibration pose
        callibration_thread = threading.Thread(target=wait_for_callibration)
        callibration_thread.start()

        calibrate_button.configure(text="Stop Calibration", state = "normal")

    elif(GlobalState().printing_state == 6):
    
        
        GlobalState().printing_state = GlobalState().previous_state
        uncallibration_thread = threading.Thread(target=uncallibrate)
        calibrate_button.configure(text="Calibrate", state = "normal")

    else:
        GlobalState().terminal_text += "print in process - continued printing"
        
    calibrate_button.configure(state = "normal")
    return

def wait_for_callibration():
    while GlobalState().printing_state == 6:
        uf.callibrationpose(GlobalState().msb)
        time.sleep(0.2)

def uncallibrate():

    #uf.commandPose(GlobalState().last_pose)

    return

def reset_but():

    global reset_button

    reset_button.configure(state="disabled")
    if(GlobalState().confirmed == False):
        print("OCCUPIED")
        reset_button.configure(state="normal")
        return
    GlobalState().confirmed == False
    

    if(GlobalState().msb == None):
        GlobalState().terminal_text += "Robot not initialized"
    else:
        GlobalState().terminal_text += "Resetting..."
        uf.reset()
        GlobalState().terminal_text += "Reset done"

    GlobalState().confirmed = True
    reset_button.configure(state="normal")


#----- tuning buttons -----

def z_up_but():
    global z_offset_textbox
    global z_offset_up_button

    z_offset_up_button.configure(state="disabled")

    if round(GlobalState().max_z_offset - GlobalState().user_z_offset, 1) < 1:
        GlobalState().terminal_text += " z_offset may not exceed" + " " + str(GlobalState().max_z_offset) + "mm in this print!"
        speed_down_button.configure(state="normal")
        return

    GlobalState().user_z_offset += GlobalState().user_z_offset_increment
    GlobalState().user_z_offset = round(GlobalState().user_z_offset, 2)
    z_offset_textbox.delete(0, ctk.END)

    # Insert the new text
    z_offset_textbox.insert(0, f'{GlobalState().user_z_offset}mm')
    print(GlobalState().user_z_offset)
    z_offset_up_button.configure(state="normal")
    return

def z_down_but():
    global z_offset_textbox
    global z_offset_down_button

    z_offset_down_button.configure(state="disabled")
    GlobalState().user_z_offset -= GlobalState().user_z_offset_increment
    GlobalState().user_z_offset = round(GlobalState().user_z_offset, 2)
    z_offset_textbox.delete(0, ctk.END)
    # Insert the new text
    z_offset_textbox.insert(0, f'{GlobalState().user_z_offset}mm')
    print(GlobalState().user_z_offset)
    z_offset_down_button.configure(state="normal")
    return

def e_speed_up_but():
    global e_speed_textbox
    global e_speed_up_button

    e_speed_up_button.configure(state="disabled")
    GlobalState().extrusion_speed_modifier += GlobalState().extrusion_speed_increment
    GlobalState().extrusion_speed_modifier = round(GlobalState().extrusion_speed_modifier, 2)
    e_speed_textbox.delete(0, ctk.END)

    # Insert the new text
    e_speed_textbox.insert(0, f'{GlobalState().extrusion_speed_modifier}%')
    print(GlobalState().extrusion_speed_modifier)
    e_speed_up_button.configure(state="normal")
    return

def e_speed_down_but():
    global e_speed_textbox
    global e_speed_down_button

    e_speed_down_button.configure(state="disabled")
    
    #check that speed does not reach 0
    if round(GlobalState().extrusion_speed_modifier - GlobalState().extrusion_speed_increment, 2) < 1:
        GlobalState().terminal_text += " Extrusion Speed may not reach 0!"
        speed_down_button.configure(state="normal")
        return

    GlobalState().extrusion_speed_modifier -= GlobalState().extrusion_speed_increment
    GlobalState().extrusion_speed_modifier = round(GlobalState().extrusion_speed_modifier, 2)
    e_speed_textbox.delete(0, ctk.END)

    # Insert the new text
    e_speed_textbox.insert(0, f'{GlobalState().extrusion_speed_modifier}%')
    e_speed_down_button.configure(state="normal")
    print(GlobalState().extrusion_speed_modifier)
    return

def speed_up_but():
    global speed_textbox
    global speed_up_button

    speed_up_button.configure(state="disabled")

    #check that speed does not reach 650 %
    if round(GlobalState().max_speed - GlobalState().printspeed_modifier, 0) < 1:
        GlobalState().terminal_text += "Speed may not exceed 650 %!"
        speed_down_button.configure(state="normal")
        return


    GlobalState().printspeed_modifier += GlobalState().printspeed_increment
    time.sleep(0.01)
    uf.adjust_speed(GlobalState().printspeed_modifier, GlobalState().msb)
    speed_textbox.delete(0, ctk.END)
    # Insert the new text
    speed_textbox.insert(0, f'{GlobalState().printspeed_modifier}%')
    speed_up_button.configure(state="normal")
    return

def speed_down_but():
    global speed_textbox
    global speed_down_button

    speed_down_button.configure(state="disabled")

    #check that speed does not reach 0
    if round(GlobalState().printspeed_modifier - GlobalState().printspeed_increment, 2) < 1:
        GlobalState().terminal_text += "Speed may not reach 0!"
        speed_down_button.configure(state="normal")
        return

    GlobalState().printspeed_modifier -= GlobalState().printspeed_increment
    time.sleep(0.01)
    uf.adjust_speed(GlobalState().printspeed_modifier, GlobalState().msb)
    speed_textbox.delete(0, ctk.END)
    # Insert the new text
    speed_textbox.insert(0, f'{GlobalState().printspeed_modifier}%')
    speed_down_button.configure(state="normal")
    return

#-------------------Helper functions-------------------
def deactivate():
    
    global terminal_text
    GlobalState().terminal_text += "Deactivating..."
    GlobalState().printing_state = 0 #0 = not printing

    #Deactivate Robot
    GlobalState().msb.WaitIdle()
    GlobalState().msb.DeactivateRobot()
    GlobalState().msb.Disconnect()
    GlobalState().msb = None
    GlobalState().terminal_text += "Deactivated Robot"
    status_update("Deactivated")
    
    return
  

# ------------------ GUI ------------------
def terminal_update():
    global terminal_text
    
    text = GlobalState().terminal_text
    last_text = "  -"
    last_index = 0
    i = 0
    while True:
        i += 1

        if(GlobalState().terminal_text == last_text):
            continue
        if GlobalState().terminal_text != "":
            #get timestamp
            current_time = datetime.now().time()
            current_time_string = current_time.strftime("%H:%M:%S")

            #print line with timestamp
            text = GlobalState().terminal_text

            #remove the text
            GlobalState().terminal_text = ""
            
            #print only the stuff that does not already exist
            terminal_text.insert(ctk.END, "[" + current_time_string + "]  " + text + "\n")
            
            last_text = text

            #scroll to the end
            terminal_text.see(tk.END)
            print(GlobalState().terminal_text)
            last_index = i
        time.sleep(0.0005)
    return

def status_update(new_status = " ? "):
    global status_text

    status_text.configure(text= new_status)

def progress_update():

    progress = 0
    current_progress = 0
    filename = os.path.basename(GlobalState().filepath)
    while(GlobalState().printing_state == 2 or GlobalState().printing_state == 3):
        if(round(GlobalState().current_progress,0) != round(progress,0)):
            progress = current_progress
            #GlobalState().terminal_text += f'Progress: {progress}%'
            
            status_update("Printing: " + str(GlobalState().current_progress) + "%\nFile: " + str(filename))

    
        time.sleep(0.1)

    return
'''
def check_rts():

    global speed_textbox
    global e_speed_textbox
    global z_offset_textbox

    progress = 0
    current_progress = 0
    filename = os.path.basename(GlobalState().filepath)


    while True:

        #progress update
        if(GlobalState().printing_state == 2 or GlobalState().printing_state == 3 or True):
            if(GlobalState().current_progress != progress):
                progress = current_progress
                #GlobalState().terminal_text += f'Progress: {progress}%'
                
                status_update("Printing: " + str(GlobalState().current_progress) + "%\nFile: " + str(filename))

    
        time.sleep(0.1)



        if(GlobalState().printing_state == 2):

            # check printspeed ---------
            textspeed = speed_textbox.get()
            valuespeed = int(textspeed.rstrip('%'))
            if(GlobalState().printspeed_modifier != valuespeed):
                if round(GlobalState().printspeed_modifier - GlobalState().printspeed_increment, 2) < 1:
                    GlobalState().terminal_text += "Speed may not reach 0!"
                    speed_textbox.delete(0, ctk.END)
                    # Insert the new text
                    speed_textbox.insert(0, f'{GlobalState().printspeed_modifier}%')
                    continue
                GlobalState().printspeed_modifier = valuespeed
                uf.adjust_speed(GlobalState().printspeed_modifier, GlobalState().msb)

                speed_textbox.delete(0, ctk.END)
                # Insert the new text
                speed_textbox.insert(0, f'{GlobalState().printspeed_modifier}%')
                print("MANUAL CHANGE")
            
            #check extrusion speed ---------
            textspeed = e_speed_textbox.get()
            valuespeed = int(textspeed.rstrip('%'))
            if(GlobalState().printspeed_modifier != valuespeed):

                if round(GlobalState().extrusion_speed_modifier - GlobalState().extrusion_speed_increment, 2) < 1:
                    GlobalState().terminal_text += " Extrusion Speed may not reach 0!"
                    e_speed_textbox.delete(0, ctk.END)

                    # Insert the new text
                    e_speed_textbox.insert(0, f'{GlobalState().extrusion_speed_modifier}%')
                    continue
                
                GlobalState().printspeed_modifier = valuespeed
                uf.adjust_speed(GlobalState().printspeed_modifier, GlobalState().msb)
                print("MANUAL CHANGE")

            #check z offset ---------
            textspeed = z_offset_textbox.get()
            valuespeed = int(textspeed.rstrip('mm'))
            if(GlobalState().user_z_offset != valuespeed):
                GlobalState().user_z_offset = valuespeed
                print("MANUAL CHANGE")
                z_offset_textbox.delete(0, ctk.END)
                # Insert the new text
                z_offset_textbox.insert(0, f'{GlobalState().user_z_offset}mm')


            time.sleep(0.11)
    return
'''
def on_z_offset_textbox_return(event):
    global z_offset_textbox
    # Get the current value of the textbox
    value = z_offset_textbox.get()
    value = float(value.rstrip('mm'))

    if(value > GlobalState().max_z_offset):
        GlobalState().terminal_text += " z_offset may not exceed" + " " + str(GlobalState().max_z_offset) + "mm in this print!"
        z_offset_textbox.delete(0, ctk.END)
        # Insert the new text
        z_offset_textbox.insert(0, f'{GlobalState().user_z_offset}mm')
        return

    GlobalState().user_z_offset = value
    z_offset_textbox.delete(0, ctk.END)
    # Insert the new text
    z_offset_textbox.insert(0, f'{GlobalState().user_z_offset}mm')
    print(f"Z offset textbox value: {value}")

    return


def on_e_speed_textbox_return(event):
    global e_speed_textbox
    # Get the current value of the textbox
    value = e_speed_textbox.get()
    value = float(value.rstrip('%'))
    if(value < 1):
        GlobalState().terminal_text += "Extrusion Speed may not reach 0!"
        e_speed_textbox.delete(0, ctk.END)
        # Insert the new text
        e_speed_textbox.insert(0, f'{GlobalState().extrusion_speed_modifier}%')
        return
    GlobalState().extrusion_speed_modifier = value
    e_speed_textbox.delete(0, ctk.END)
    # Insert the new text
    e_speed_textbox.insert(0, f'{GlobalState().extrusion_speed_modifier}%')
    print(f"e_speed_value: {value}")

    return

def on_speed_textbox_return(event):
    global speed_textbox
    # Get the current value of the textbox
    value = speed_textbox.get()
    value = float(value.rstrip('%'))

    if(value > GlobalState().max_speed):
        GlobalState().terminal_text += "Speed may not exceed 650%!"
        speed_textbox.delete(0, ctk.END)
        # Insert the new text
        speed_textbox.insert(0, f'{GlobalState().printspeed_modifier}%')
        return
    
    if(value < 1):
        GlobalState().terminal_text += "Speed may not reach 0!"
        speed_textbox.delete(0, ctk.END)
        # Insert the new text
        speed_textbox.insert(0, f'{GlobalState().printspeed_modifier}%')
        return
    GlobalState().printspeed_modifier = value
    speed_textbox.delete(0, ctk.END)
    # Insert the new text
    speed_textbox.insert(0, f'{GlobalState().printspeed_modifier}%')
    uf.adjust_speed(GlobalState().printspeed_modifier, GlobalState().msb)
    print(f"speed_value: {value}")

    return


def search_file(filename):

    
    # Get the directory of the script
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    
    # Get the parent directory
    parent_directory = os.path.dirname(script_directory)
    
    # Search for the file in the script directory and the parent directory
    for directory in [script_directory, parent_directory]:
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            break
    else:
        print(f"Could not find {filename}")
        filepath = None
        return filepath

    if filepath is not None:
        return filepath
    
#main gui function
def init_gui():
    
    #define soime parameters
    leftcol = 0.05
    rightcol = 0.28
    rcol = 0.78
    buttoncolor = '#0859C3'

    ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
    ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

    root = ctk.CTk()  # create CTk window like you do with the Tk window
    root.geometry("800x450")
    root.title("SonoBone control interface")
    #root.iconbitmap(r"C:\Users\steph\OneDrive\_Studium\_Semester 6 (FS2024)\Bachelor Thesis\CODEBASE\BachelorThesis_SonoBone\SonoBone_icon.ico")
    root.iconbitmap(search_file("SonoBone_icon.ico"))

    #initialize all the gui parts
    print_control(root, leftcol,rightcol,buttoncolor,rcol)
    print_monitor(root, leftcol,rightcol,buttoncolor,rcol)
    cosmetics(root, leftcol,rightcol,buttoncolor,rcol)
    tuning(root, leftcol,rightcol,buttoncolor,rcol)

    #start the terminal update thread
    update_terminal_thread = threading.Thread(target=terminal_update)
    update_terminal_thread.start()

    
    # Bind the function to the <Return> event for the e_speed_textbox
    e_speed_textbox.bind('<Return>', on_e_speed_textbox_return)
    z_offset_textbox.bind('<Return>', on_z_offset_textbox_return)
    speed_textbox.bind('<Return>', on_speed_textbox_return)

    threads_activated = False


    #start gui
    root.mainloop()
    

    

