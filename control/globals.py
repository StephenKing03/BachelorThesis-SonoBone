# globals.py

class GlobalState:
    #singeleton class
    _instance = None
  
    #printing_state - RT variable for print status information
    printing_state = 0 #0: uninitialized, 1:initialized, 2:printing, 3: paused 4: finished  5: stopped 6: calibration 7: error

    occupied = False
    error = 0

    #user_z_offset - RT variable for z offset tuning
    user_z_offset = 0
    user_z_offset_increment = 0.1
    max_z_offset = 10
    max_speed = 650

    #printspeed - RT variable for print speed tuning
    printspeed_modifier = 20 #% 
    printspeed_increment = 5

    #extrusion speed modifier
    extrusion_speed_modifier = 100 #%
    extrusion_speed_increment = 5

    #extrusion direction
    extrusion_direction = 1
    
    #filepath for the currently printed file
    filepath = " "
    
    #terminal_text - RT variable for terminal output, gets added on top
    terminal_text = "Terminal activated "
    status_text = ""
    current_progress = 0

    threshold = 0.3

    #target position stack for smooth printing
    target_positions = None
    sending_to_arduino = False

    
    last_pose = [130, 0, 100, 180, 0, -180]
    last_base_angle = 0
    previous_state = 0
    last_extruder_pos = 0

    arduino_info = [None]

    #progress
    current_line = 0
    displaying_preview = False 
    coordinates = []
    cartesian_coordinates = []
    

    #msb - Robot instance - for referencing the robot   
    msb = None
    arduino_port = None

    

    #singeleton class
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(GlobalState, cls).__new__(cls, *args, **kwargs)
        return cls._instance



class RobotStats:
    def __init__(self):
        self.min_z = -4.9 + 1.3 - 0.6
        self.max_z = 100
        self.min_x = 110
        self.max_x = 170
        self.min_y = -40
        self.max_y = 40

        self.diameter = 90
        self.center_x = (170-110)/2 + 110
        self.center_y = 0

        self.tooloffset_x = 0
        self.tooloffset_y = 0
        self.tooloffset_z = 93 
        self.tooloffset_alpha = 0
        self.tooloffset_beta = 0
        self.tooloffset_gamma = 0
        
        self.joint_vel_limit = 30 #starts to have effect from 50 % or below
        self.start_joint_vel_limit = 100
        
        self.max_linvel = 5 #this does not seem to do anything, even if directly sent to robot ...
        
        self.max_lin_acc = 500
        self.max_acc = 500
        self.print_offset_x = 0
        self.print_offset_y = 0

        self.max_semaphores = 3 #not used 

        self.extrusion_speed = 1000 #mm/min

        self.portname = "COM27"



    


    