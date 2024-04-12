import customtkinter as ctk
import tkinter as tk
import string
import os
import threading
import time
from datetime import datetime
import mecademicpy.robot as mdr
from PIL import Image, ImageTk

from tkinter import filedialog

import utility_functions as uf  # import utility functions
import gcode_translator as gt  # import gcode translator

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

def print_control(root, leftcol, rightcol, buttoncolor, rcol):
    #button to initialize the robot
    init_button = ctk.CTkButton(master=root, text="Initialize Robot", font=("Avenir Heavy",15), fg_color= buttoncolor, command=init_print_but)
    init_button.place(relx=leftcol, rely=0.35, anchor=ctk.NW)

    #button to set file path
    file_button = ctk.CTkButton(master=root, text="Select File", font=("Avenir Heavy",15),fg_color= '#089DC3', command=select_file_but)
    file_button.place(relx=leftcol, rely=0.45, anchor=ctk.NW)

    #button to start printing
    start_button = ctk.CTkButton(master=root, text="Start Printing", font=("Avenir Heavy",15),fg_color= buttoncolor, command=start_print_but)
    start_button.place(relx=leftcol, rely=0.55, anchor=ctk.NW)

    #button to stop printing
    start_button = ctk.CTkButton(master=root, text="Stop Printing", font=("Avenir Heavy",15), fg_color= '#DC0F24' ,command=stop_print_but)
    start_button.place(relx=leftcol, rely=0.65, anchor=ctk.NW)

    #button to pause and resume printing
    global pause_button
    pause_button = ctk.CTkButton(master=root, text="Pause Printing", font=("Avenir Heavy",15), fg_color= buttoncolor, command=pause_print_but)
    pause_button.place(relx=leftcol, rely=0.9, anchor=ctk.NW)

    #button to callibrate the robot
    calibrate_button = ctk.CTkButton(master=root, text="Calibrate", font=("Avenir Heavy",15), fg_color= buttoncolor, command=calibration_but)
    calibrate_button.place(relx=leftcol, rely=0.75, anchor=ctk.NW)

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
    #status_text.configure(text = "Deactivated")

    #terminal info
    terminal_label = ctk.CTkLabel(master=root, text="Print info", font=("Avenir Heavy", 15, 'bold'), width = 40, pady = 10, anchor = 'center')
    terminal_label.place(relx=rightcol, rely=0.18, anchor=ctk.NW)

    terminal_text = tk.Text(master=root, font=("Avenir",12), height=26, width=57, bg = '#1A0F10', fg = '#FFFFFF')
    terminal_text.place(relx=rightcol, rely=0.25, anchor=ctk.NW)

    scrollbar = tk.Scrollbar(root, command=terminal_text.yview, background = 'blue')
    scrollbar.place(relx=rcol -0.07, rely=0.25, anchor=ctk.NW, height=root.winfo_screenheight()*0.59)
    terminal_text['yscrollcommand'] = scrollbar.set

    terminal_text.insert(ctk.END, "")

    return

def cosmetics(root, leftcol, rightcol, buttoncolor, rcol):

    #title
    info_title = ctk.CTkLabel(master=root, text="SonoBone control interface", font=("Avenir Heavy", 31, 'bold'), fg_color= '#333332', width = root.winfo_screenwidth(), pady = 5, anchor = 'center')
    info_title.place(relwidth = 1)

    #cool icon
    image = Image.open(r"C:\Users\steph\OneDrive\_Studium\_Semester 6 (FS2024)\Bachelor Thesis\CODEBASE\BachelorThesis_SonoBone\cool_robot_icon.png")
    image  = image.resize((70,70))
    photo = ImageTk.PhotoImage(image)
    icon_label = ctk.CTkLabel(master=root, image=photo,fg_color= '#333332', text = "")
    icon_label.place(relx=0.12, rely=0.015, anchor=ctk.NW)

    return

def tuning(root, leftcol, rightcol, buttoncolor, rcol):

    global z_offset_textbox
    global speed_textbox

    #set z offsetbutton up and down
    z_offset_up_button = ctk.CTkButton(master=root, text="↑", font=("Avenir Heavy",15), fg_color= buttoncolor, command=z_up_but, width = 50, height = 25, anchor = 'center')
    z_offset_up_button.place(relx=rcol, rely=0.25, anchor=ctk.NW)
    z_offset_down_button = ctk.CTkButton(master=root, text="↓", font=("Avenir Heavy",15), fg_color= buttoncolor, command=z_down_but, width = 50, height = 25, anchor = 'center')
    z_offset_down_button.place(relx=rcol, rely=0.45, anchor=ctk.NW)

    #z offset textbox
    z_offset_textbox = ctk.CTkEntry(master=root, font=("Avenir", 10), width=50)
    z_offset_textbox.place(relx=rcol, rely=0.35, anchor=ctk.NW)
    # Set the text of z_offset_textbox
    z_offset_textbox.insert(0, GlobalState().user_z_offset)

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
    speed_textbox.insert(0, f'{GlobalState().printspeed}mm/s')

    speed_label= ctk.CTkLabel(master=root, text="Speed", font=("Avenir Heavy", 15, 'bold'), width = 40, anchor = 'center')
    speed_label.place(relx=rcol, rely=0.56, anchor=ctk.NW)

    return

#------------------ Button functions ------------------

def start_print_but():
    
    #in case of restart - make sure it does not shut down again
    GlobalState().exit_program = False

    #check if file path is set:
    if GlobalState().filepath == " ":
        GlobalState().terminal_text +="Error: No file selected \n"
        return 
    
    #Extract coordinates
    status_update("Extracting cordinates ...")
    GlobalState().terminal_text += "Extracting coordinates from file...  \n"
    coordinates = gt.extract_coordinates(GlobalState().filepath)
    time.sleep(2)
    GlobalState().terminal_text += " --done!\n"
    
    #set starting position
    uf.startpose(GlobalState().msb)

    #start printing with thread so that gui still works
    GlobalState().printing_state = 2 #2 = printing
    filename = os.path.basename(GlobalState().filepath)
    status_update("Printing ...  \nFile: " + str(filename))
    GlobalState().msb.WaitIdle()
    print_thread = threading.Thread(target=gt.write_coordinates, args=(coordinates, GlobalState().msb))
    print_thread.start()

    #start position checking thread
    check_thread = threading.Thread(target=uf.check_target_pose)
    check_thread.start()
    
    #wait for program to finish to update the text
    finished_thread = threading.Thread(target=wait_for_printing)
    finished_thread.start()

    return
    
def stop_print_but():
    
    GlobalState().printing_state = 0 #0 = not printing
    status_update(text="Print stopped")
    GlobalState().exit_program = True #leads to writecoordinates and the exit condition
    deactivate()
    return

def init_print_but():
   
    #set states and info text
    GlobalState().printing_state = 0 #0 = not printing

    #connect to robot if the robot is not connected already (e.g. from reset)
    if(GlobalState().msb == None):
        GlobalState().msb = mdr.Robot() #msb = MegaSonoBot # instance of the robot class
        GlobalState().msb.Connect(address='192.168.0.100') #using IP address of the robot and Port 10000 to control
        GlobalState().msb.ActivateRobot() #same as in the webinterface: activate Robot
        GlobalState().msb.Home() #Home the robot
    
    msb = GlobalState().msb
    #setup robot 
    msb.ClearMotion()
    msb.SendCustomCommand("SetRealTimeMonitoring('cartpos')") #start logging position
    msb.SendCustomCommand('ResetError()')
    msb.SendCustomCommand('ResumeMotion()')
    msb.SendCustomCommand(f'SetJointVelLimit({RobotStats().joint_vel_limit})')
    msb.SendCustomCommand(f'SetCartLinVel({RobotStats().max_linvel})')
    msb.SendCustomCommand(f'SetCartAcc({RobotStats().max_acc}')
    msb.SendCustomCommand('SetBlending(70)')
    #Set tooltip reference frame to 160 in front of the end of robot arm
    msb.SendCustomCommand(f'SetTrf({RobotStats().tooloffset_x},{RobotStats().tooloffset_y},{RobotStats().tooloffset_z},{RobotStats().tooloffset_alpha},{RobotStats().tooloffset_beta},{RobotStats().tooloffset_gamma})')

    
    #setpayload!!!!!--------------------------------

    msb.WaitIdle()
    #msb.StartLogging(0.001)

    #send info text
    msb.WaitIdle()
    time.sleep(1)

    #start the terminal thread
    terminal_thread = threading.Thread(target=terminal_update)
    terminal_thread.start()

    #show that terminal is activated
    #GlobalState().terminal_text += "Terminal activated \n"

    #wait for the initialization to finish
    GlobalState().msb.WaitIdle()

    #set the robot to cleanpose
    uf.cleanpose(GlobalState().msb)
    GlobalState().msb.WaitIdle()

    GlobalState().printing_state = 1 #1 = ready to print
    status_update("Ready to print")
    GlobalState().terminal_text += "Robot activated and ready to go!\n"

    return

def select_file_but():
    
    #get the file path
    file_path = filedialog.askopenfilename()
    #print("Selected file:", file_path)

    # save the file path into GlobalState().filepath for later use
    GlobalState().filepath = file_path
    filename = os.path.basename(file_path)
    status_update("File selected:\n'"  + filename + "'")
    GlobalState().terminal_text += f"File selected: '{filename}'\r\n"

    return

def pause_print_but():
    global pause_button
    if(GlobalState().printing_state == 2):

        status_update("Printing paused")
        GlobalState().printing_state = 3 #3 = paused
        GlobalState().terminal_text += "Printing paused\n"

        time.sleep(2)
        pause_button.configure(text="Resume Printing")

    else:
        status_update("Printing...")
        GlobalState().printing_state = 2 #2 = printing
        GlobalState().terminal_text += "Printing resumed\n"

        time.sleep(0.1)
        pause_button.configure(text="Pause Printing")

    return

def calibration_but():

    
    status_update("Calibrating...")
    uf.callibrationpose(GlobalState().msb)

    return

#----- tuning buttons -----

def z_up_but():
    global z_offset_textbox
    GlobalState().user_z_offset += GlobalState().user_z_offset_increment
    GlobalState().user_z_offset = round(GlobalState().user_z_offset, 2)
    z_offset_textbox.delete(0, ctk.END)

    # Insert the new text
    z_offset_textbox.insert(0, f'{GlobalState().user_z_offset}mm')
    print(GlobalState().user_z_offset)
    return

def z_down_but():
    global z_offset_textbox
    GlobalState().user_z_offset -= GlobalState().user_z_offset_increment
    GlobalState().user_z_offset = round(GlobalState().user_z_offset, 2)
    z_offset_textbox.delete(0, ctk.END)
    # Insert the new text
    z_offset_textbox.insert(0, f'{GlobalState().user_z_offset}mm')
    print(GlobalState().user_z_offset)
    return

def speed_up_but():
    global speed_textbox
    GlobalState().printspeed += GlobalState().printspeed_increment
    uf.adjust_speed(GlobalState().printspeed, GlobalState().msb)
    speed_textbox.delete(0, ctk.END)
    # Insert the new text
    speed_textbox.insert(0, f'{GlobalState().printspeed}mm/s')
    return

def speed_down_but():
    global speed_textbox
    GlobalState().printspeed -= GlobalState().printspeed_increment
    uf.adjust_speed(GlobalState().printspeed, GlobalState().msb)
    speed_textbox.delete(0, ctk.END)
    # Insert the new text
    speed_textbox.insert(0, f'{GlobalState().printspeed}mm/s')
    return

#-------------------Helper functions-------------------
def deactivate():
    
    global terminal_text
    status_update("Deactivating ...")
    GlobalState().terminal_text += "Deacticating\n"
    GlobalState().printing_state = 0 #0 = not printing

    #Deactivate Robot
    GlobalState().msb.WaitIdle()
    GlobalState().msb.DeactivateRobot()
    GlobalState().msb.Disconnect()
    GlobalState().terminal_text += "Deactivated Robot\n"
    status_update("Deactivated")
    

    return

def wait_for_printing():
    while GlobalState().printing_state != 3:
        time.sleep(0.1)
    GlobalState().terminal_text += "-------------------PRINT FINISHED-------------\n"
    
    status_update("Finished printing!\n - ready to print again")
    
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
            terminal_text.insert(ctk.END, "[" + current_time_string + "]  " + text)
            
            last_text = text

            #scroll to the end
            terminal_text.see(tk.END)
            print(GlobalState().terminal_text)
            last_index = i
        time.sleep(0.005)

        #compare current text with previous text line by line
        #if different, add the new line to the terminal_text
        
            
    return


def status_update(new_status = " ? "):
    global status_text

    status_text.configure(text= new_status)
    time.sleep(0.2)

#main gui function
def init_gui():
    
    #define soime parameters
    leftcol = 0.05
    rightcol = 0.32
    rcol = 0.88
    buttoncolor = '#0859C3'

    ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
    ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

    root = ctk.CTk()  # create CTk window like you do with the Tk window
    root.geometry("700x450")
    root.title("SonoBone control interface")
    root.iconbitmap(r"C:\Users\steph\OneDrive\_Studium\_Semester 6 (FS2024)\Bachelor Thesis\CODEBASE\BachelorThesis_SonoBone\SonoBone_icon.ico")


    #initialize all the gui parts
    print_control(root, leftcol,rightcol,buttoncolor,rcol)
    print_monitor(root, leftcol,rightcol,buttoncolor,rcol)
    cosmetics(root, leftcol,rightcol,buttoncolor,rcol)
    tuning(root, leftcol,rightcol,buttoncolor,rcol)

    #start the terminal update thread
    update_terminal_thread = threading.Thread(target=terminal_update)
    update_terminal_thread.start()


    #start gui
    root.mainloop()

    print("tests")
    

    

