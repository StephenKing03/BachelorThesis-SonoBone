# globals.py

class GlobalState:
    _instance = None
    exit_program = False
    user_z_offset = 0

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(GlobalState, cls).__new__(cls, *args, **kwargs)
        return cls._instance



class RobotStats:
    def __init__(self):
        self.min_z = -55 #-68
        self.max_z = 100
        self.min_x = 130
        self.max_x = 210
        self.min_y = -90
        self.max_y = 70

        self.tooloffset_x = 0
        self.tooloffset_y = 0
        self.tooloffset_z = 110 +30 #was 182.4
        self.tooloffset_alpha = 0
        self.tooloffset_beta = 0
        self.tooloffset_gamma = 0
        
        self.joint_vel_limit = 10
        self.max_linvel = 5
        self.joint_vel_limit_start = 100
        self.max_linvel_start = 30

        self.print_offset_x = 0
        self.print_offset_y = 0

    