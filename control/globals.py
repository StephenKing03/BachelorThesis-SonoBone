# globals.py

class GlobalState:
    _instance = None
    exit_program = False
    
    printing_state = 0 #0: not printing, 1:ready 2:printing, 3: paused 3: finished 4: error 5: stopped
    user_z_offset = 0
    user_z_offset_increment = 0.05
    
    filepath = " "
    
    terminal_text = "terminal activated \n "
    status = 0
    printspeed = 10 #mm/s #adjust also RobotStats
    printspeed_increment = 1


    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(GlobalState, cls).__new__(cls, *args, **kwargs)
        return cls._instance



class RobotStats:
    def __init__(self):
        self.min_z = -35 #-68 and then -55
        self.max_z = 100
        self.min_x = 130
        self.max_x = 210
        self.min_y = -90
        self.max_y = 70

        self.tooloffset_x = 0
        self.tooloffset_y = 0
        self.tooloffset_z = 50 #was 182.4 and then 110+30
        self.tooloffset_alpha = 0
        self.tooloffset_beta = 0
        self.tooloffset_gamma = 0
        
        self.joint_vel_limit = 10
        self.max_linvel = 10
        self.joint_vel_limit_start = 100
        self.max_linvel_start = 30
        self.max_lin_acc = 100  

        self.print_offset_x = -50
        self.print_offset_y = 20
        self.msb = None

    


    