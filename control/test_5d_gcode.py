import math
import time #for time.sleep()
import utility_functions as uf #import utility functions
from utility_functions import RobotStats
import rt_user_functions as ruf #extra functions such as 'exiting'


#---extract the coordinates from the gcode file---------------------------------------------------------
def d5_extract_coordinates(file_path):
    coordinates = []

    
    with open(file_path, 'r') as file:
        
        for line in file:
            i = 0
            x = None
            y = None
            z = None
            alpha = None
            beta = None
            gamma = None
            for command in line.split():
                if (i == 0):
                    x = float(command[1:])
                if(i == 1):
                    y = float(command[1:])
                if(i == 2):
                    z = float(command[1:])
                if(i == 3):
                    alpha = float(command[1:])
                if(i == 4):
                    beta = float(command[1:])
                if(i == 5):
                    gamma = float(command[1:])
                i += 1
            coordinates.append([x,y,z,alpha,beta,gamma])
                    
                
    return coordinates


#---write the coordinates (2D print) to the robot ---------------------------------------------------------
def d5_write_coordinates(coordinates, self):
    
    #set printing speed
    self.SendCustomCommand(f'SetJointVelLimit({RobotStats.joint_vel_limit})')
    self.SendCustomCommand(f'SetCartLinVel({RobotStats.max_linvel})')


    #coordinates consist of [x, y, z, e, er]        
    z_0 = RobotStats.min_z 
    x_offset = RobotStats.min_x + RobotStats.print_offset_x
    y_offset = RobotStats.min_y + RobotStats.print_offset_y
    non_none_z = 0
    non_none_x = 0
    non_none_y = 0
    i = 0

    #set starting position
    uf.startpose(self)
    
    
    for x, y, z, a, b, c in coordinates:
        
        print(f'--{i}--')
        
        # Check exit_program.value instead of exit_program
        if ruf.GlobalState().exit_program:  
            
            print('BREAK - exitprogram')
            uf.cleanpose(self)
            time.sleep(10)
            break
        i += 1

        uf.commandPose(x+x_offset, y+y_offset, non_none_z + z_0 + ruf.GlobalState().user_z_offset, a, b, c, self)

        self.WaitIdle()
        time.sleep(0.1)
    #-------------------finished print -----------------------------
    uf.endpose(self)

    return


