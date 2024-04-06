import customtkinter as tk
import string
import os
import threading
import time

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

def print_control(root, leftcol, rightcol, buttoncolor, rcol):
    #button to initialize the robot
    init_button = tk.CTkButton(master=root, text="Initialize Robot", font=("Avenir Heavy",15), fg_color= buttoncolor, command=init_print_but)
    init_button.place(relx=leftcol, rely=0.50, anchor=tk.NW)

    #button to set file path
    file_button = tk.CTkButton(master=root, text="Select File", font=("Avenir Heavy",15),fg_color= '#089DC3', command=select_file)
    file_button.place(relx=leftcol, rely=0.35, anchor=tk.NW)

    #button to start printing
    start_button = tk.CTkButton(master=root, text="Start Printing", font=("Avenir Heavy",15),fg_color= buttoncolor, command=start_print_but)
    start_button.place(relx=leftcol, rely=0.65, anchor=tk.NW)

    #button to stop printing
    start_button = tk.CTkButton(master=root, text="Stop Printing", font=("Avenir Heavy",15), fg_color= '#DC0F24' ,command=stop_print_but)
    start_button.place(relx=leftcol, rely=0.80, anchor=tk.NW)

    return

def print_monitor(root, leftcol, rightcol, buttoncolor, rcol):

    global status_text
    global terminal_text

    #status info
    status_label = tk.CTkLabel(master=root, text="Status:", font=("Avenir Heavy", 15, 'bold'), width = 40, pady = 10, anchor = 'center')
    status_label.place(relx=leftcol, rely=0.18, anchor=tk.NW)

    status_text = tk.CTkLabel(master=root, text = " - ", font=("Avenir Heavy",12), height=4, width=450, anchor = tk.W)
    status_text.place(relx=leftcol, rely=0.25, anchor=tk.NW)

    status_text.configure(text = "waiting...")

    #terminal info
    terminal_label = tk.CTkLabel(master=root, text="Print info", font=("Avenir Heavy", 15, 'bold'), width = 40, pady = 10, anchor = 'center')
    terminal_label.place(relx=rightcol, rely=0.18, anchor=tk.NW)

    terminal_text = tk.CTkLabel(master=root, text = " - ", font=("Avenir",12), height=root.winfo_screenheight()*0.35, width=350,fg_color = '#1A0F10', anchor = tk.NW)
    terminal_text.place(relx=rightcol, rely=0.25, anchor=tk.NW)

    terminal_text.configure(text = " ")

    return

def cosmetics(root, leftcol, rightcol, buttoncolor, rcol):
    #title

    info_title = tk.CTkLabel(master=root, text="SonoBone control interface", font=("Avenir Heavy", 25, 'bold'), fg_color= '#333332', width = root.winfo_screenwidth(), pady = 20, anchor = 'center')
    info_title.place(relwidth = 1)

    return


def tuning(root, leftcol, rightcol, buttoncolor, rcol):

    global z_offset_textbox
    global speed_textbox

    #set z offsetbutton up and down
    z_offset_up_button = tk.CTkButton(master=root, text="↑", font=("Avenir Heavy",15), fg_color= buttoncolor, command=z_up_but, width = 50, height = 25, anchor = 'center')
    z_offset_up_button.place(relx=rcol, rely=0.25, anchor=tk.NW)
    z_offset_down_button = tk.CTkButton(master=root, text="↓", font=("Avenir Heavy",15), fg_color= buttoncolor, command=z_down_but, width = 50, height = 25, anchor = 'center')
    z_offset_down_button.place(relx=rcol, rely=0.45, anchor=tk.NW)

    #z offset textbox
    z_offset_textbox = tk.CTkEntry(master=root, font=("Avenir", 10), width=50)
    z_offset_textbox.place(relx=rcol, rely=0.35, anchor=tk.NW)
    # Set the text of z_offset_textbox
    z_offset_textbox.insert(0, GlobalState().user_z_offset)

    z_offset_label= tk.CTkLabel(master=root, text="Z-offset", font=("Avenir Heavy", 15, 'bold'), width = 40, anchor = 'center')
    z_offset_label.place(relx=rcol, rely=0.18, anchor=tk.NW)

    #set speed button up and down
    speed_up_button = tk.CTkButton(master=root, text="↑", font=("Avenir Heavy",15), fg_color= buttoncolor, command=speed_up_but, width = 50, height = 25)
    speed_up_button.place(relx=rcol, rely=0.63, anchor=tk.NW)
    speed_down_button = tk.CTkButton(master=root, text="↓", font=("Avenir Heavy",15), fg_color= buttoncolor, command=speed_down_but, width = 50, height = 25, anchor = 'center')
    speed_down_button.place(relx=rcol, rely=0.83, anchor=tk.NW)

    #speed textbox
    speed_textbox = tk.CTkEntry(master=root, font=("Avenir", 10), width=50)
    speed_textbox.place(relx=rcol, rely=0.73, anchor=tk.NW)
    speed_textbox.insert(0, f'{GlobalState().printspeed}mm/s')

    speed_label= tk.CTkLabel(master=root, text="Speed", font=("Avenir Heavy", 15, 'bold'), width = 40, anchor = 'center')
    speed_label.place(relx=rcol, rely=0.56, anchor=tk.NW)

    return

#------------------ Button functions ------------------

def start_print_but():
    global status_text

    #in case of restart - make it not shut down again
    GlobalState().exit_program = False

    #check if file path is set:
    if GlobalState().filepath == " ":
        terminal_text.configure(text="Error: No file selected")
        return False
    
    #Extract coordinates
    status_text.configure(text="Extracting cordinates ...")
    GlobalState().terminal_text += "Extracting coordinates from file"
    coordinates = gt.extract_coordinates(GlobalState().filepath)
    GlobalState().terminal_text += "--done\n"
    
    #start printing with thread so that gui still works
    GlobalState().printing_state = 2 #2 = printing
    status_text.configure(text="Printing ...")
    print_thread = threading.Thread(target=gt.write_coordinates, args=(coordinates, GlobalState().msb))
    print_thread.start()
    
    #printing finished
    GlobalState().terminal_text += "--done\n"
    status_text.configure(text="Finished printing!")
    
    return
    

def stop_print_but():
    global status_text

    GlobalState().printing_state = 0 #0 = not printing
    status_text.configure(text="print stopped")
    GlobalState().exit_program = True
    return


def init_print_but():
    global status_text
    
    #set states and info text
    GlobalState().printing_state = 0 #0 = not printing
    status_text.configure(text="Initializing robot...")
    
    #--from utility function - activation sequence()--

    #connect to robot if the robot is not connected already (e.g. from reset)
    if GlobalState().msb == None:
        GlobalState().msb = mdr.Robot() #msb = MegaSonoBot # instance of the robot class
        GlobalState().msb.Connect(address='192.168.0.100') #using IP address of the robot and Port 10000 to control
        GlobalState().ActivateRobot() #same as in the webinterface: activate Robot
        GlobalState().Home() #Home the robot
    
    
    #setup robot 
    msb.ClearMotion()
    msb.SendCustomCommand('ResetError()')
    msb.SendCustomCommand('ResumeMotion()')
    msb.SendCustomCommand(f'SetJointVelLimit({RobotStats.joint_vel_limit_start})')
    msb.SendCustomCommand(f'SetCartLinVel({RobotStats.max_lin_acc})')
    msb.SendCustomCommand(f'SetCartLinVel({RobotStats.max_linvel_start})')
    msb.SendCustomCommand('SetBlending(40)')
    #Set tooltip reference frame to 160 in front of the end of robot arm
    msb.SendCustomCommand(f'SetTrf({RobotStats.tooloffset_x},{RobotStats.tooloffset_y},{RobotStats.tooloffset_z},{RobotStats.tooloffset_alpha},{RobotStats.tooloffset_beta},{RobotStats.tooloffset_gamma})')

    
    #setpayload!!!!!--------------------------------

    #send info text
    msb.WaitIdle()
    print('Robot activated and ready to go!')
    time.sleep(1)

    #start the terminal thread
    terminal_thread = threading.Thread(target=terminal_update)
    terminal_thread.start()
    GlobalState().terminal_text += "Terminal activated \n"
    GlobalState().msb.WaitIdle()

    #set the robot to cleanpose
    status_text.configure(text="Robot initialized")
    uf.cleanpose(GlobalState().msb)
    GlobalState().msb.WaitIdle()

    GlobalState().printing_state = 1 #1 = ready to print
    status_text.configure(text="Ready to print")
    GlobalState().terminal_text += "Robot activated and ready to go\n"

    return


def reset():
    global status_text
    global terminal_text
    status_text.configure(text="Resetting ...")
    GlobalState().printing_state = 0 #0 = not printing

    # Reset the robot
    uf.deactivationsequence(GlobalState().msb)
    init_print_but()
    terminal_text.configure(text="Reset complete!")

    return

def select_file():
    global status_text

    #get the file path
    file_path = filedialog.askopenfilename()
    print("Selected file:", file_path)

    # save the file path into GlobalState().filepath for later use
    GlobalState().filepath = file_path
    filename = os.path.basename(file_path)
    status_text.configure(text="File selected: \n"  + filename)
    GlobalState().terminal_text += f"File selected: {filename}\r\n"

    return


#----- tuning buttons -----

def z_up_but():
    global z_offset_textbox
    GlobalState().user_z_offset += GlobalState().user_z_offset_increment
    GlobalState().user_z_offset = round(GlobalState().user_z_offset, 2)
    z_offset_textbox.delete(0, tk.END)

    # Insert the new text
    z_offset_textbox.insert(0, f'{GlobalState().user_z_offset}mm')
    print(GlobalState().user_z_offset)
    return

def z_down_but():
    global z_offset_textbox
    GlobalState().user_z_offset -= GlobalState().user_z_offset_increment
    GlobalState().user_z_offset = round(GlobalState().user_z_offset, 2)
    z_offset_textbox.delete(0, tk.END)
    # Insert the new text
    z_offset_textbox.insert(0, f'{GlobalState().user_z_offset}mm')
    print(GlobalState().user_z_offset)
    return


def speed_up_but():
    global speed_textbox
    GlobalState().printspeed += GlobalState().printspeed_increment
    speed_textbox.delete(0, tk.END)
    # Insert the new text
    speed_textbox.insert(0, f'{GlobalState().printspeed}mm/s')
    return

def speed_down_but():
    global speed_textbox
    GlobalState().printspeed -= GlobalState().printspeed_increment
    speed_textbox.delete(0, tk.END)
    # Insert the new text
    speed_textbox.insert(0, f'{GlobalState().printspeed}mm/s')
    return


# ------------------ GUI ------------------

def terminal_update():
    text = GlobalState().terminal_text
    while True:
        if GlobalState().terminal_text != text:
            terminal_text.configure(text=GlobalState().terminal_text)
            text = GlobalState().terminal_text
        time.sleep(0.5)
    return

def speed_update():
   
    speed = GlobalState().printspeed
    while True:
        if speed != GlobalState().printspeed:
            speed = GlobalState().printspeed_increment
            uf.adjust_speed(GlobalState().printspeed)

    return False
    return

def status_update():
    text = GlobalState().status_text
    while True:
        if GlobalState().status_text != text:
            status_text.configure(text=GlobalState().status_text)
            text = GlobalState().status_text
        time.sleep(0.5)
    return

def init_gui():
    
    #define soime parameters
    leftcol = 0.05
    rightcol = 0.35
    rcol = 0.88
    buttoncolor = '#0859C3'

    tk.set_appearance_mode("System")  # Modes: system (default), light, dark
    tk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

    root = tk.CTk()  # create CTk window like you do with the Tk window
    root.geometry("700x420")
    root.title("SonoBone control interface")


    #initialize all the gui parts
    print_control(root, leftcol,rightcol,buttoncolor,rcol)
    print_monitor(root, leftcol,rightcol,buttoncolor,rcol)
    cosmetics(root, leftcol,rightcol,buttoncolor,rcol)
    tuning(root, leftcol,rightcol,buttoncolor,rcol)

    #start the terminal update thread
    update_terminal_thread = threading.Thread(target=terminal_update)
    update_terminal_thread.start()

    

    root.mainloop()

    print("tests")
    

    

