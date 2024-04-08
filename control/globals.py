# globals.py

class GlobalState:
    #singeleton class
    _instance = None

    #exit_program - RT variable to stop the printing
    exit_program = False
    
    #printing_state - RT variable for print status information
    printing_state = 0 #0: not printing, 1:ready 2:printing, 3: paused 3: finished 4: error 5: stopped

    #user_z_offset - RT variable for z offset tuning
    user_z_offset = 0
    user_z_offset_increment = 0.5

    #printspeed - RT variable for print speed tuning
    printspeed = 10 #mm/s #adjust also RobotStats
    printspeed_increment = 1
    
    #filepath for the currently printed file
    filepath = " "
    
    #terminal_text - RT variable for terminal output, gets added on top
    terminal_text = " "
    status_text = " "

    threshold = 0.1

    #msb - Robot instance - for referencing the robot   
    msb = None


    #singeleton class
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(GlobalState, cls).__new__(cls, *args, **kwargs)
        return cls._instance



class RobotStats:
    def __init__(self):
        self.min_z = -55 #-68 and then -55
        self.max_z = 100
        self.min_x = 130
        self.max_x = 210
        self.min_y = -90
        self.max_y = 70

        self.tooloffset_x = 0
        self.tooloffset_y = 0
        self.tooloffset_z = 110+30 #was 182.4 and then 110+30
        self.tooloffset_alpha = 0
        self.tooloffset_beta = 0
        self.tooloffset_gamma = 0
        
        self.joint_vel_limit = 10
        self.max_linvel = 10
        self.joint_vel_limit_start = 100
        self.max_linvel_start = 30
        self.max_lin_acc = 100  
        self.max_acc = 10

        self.print_offset_x = 0
        self.print_offset_y = 0
    

    


    