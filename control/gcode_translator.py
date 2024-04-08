import math
import time #for time.sleep()
import utility_functions as uf #import utility functions
from utility_functions import RobotStats
from globals import GlobalState


#---extract the coordinates from the gcode file---------------------------------------------------------
def extract_coordinates(file_path):
    coordinates = []

    
    with open(file_path, 'r') as file:
        i = 0
        for line in file:
            if i <44:
                i+=1
                continue
            if line.startswith(';TIME_ELAPSED'):
                break
            if line.startswith('G0') or line.startswith('G1'):
                x = None
                y = None
                z = None
                alpha = None
                beta = None
                gamma = None
                e = None
                er = False
                for command in line.split():
                    if command.startswith('X'):
                        x = float(command[1:])
                    elif command.startswith('Y'):
                        y = float(command[1:])
                    elif command.startswith('Z'):
                        try:
                            z = float(command[1:])
                        except:
                            er = True
                    elif command.startswith('E'):
                        e = float(command[1:])
                coordinates.append([x, y, z, e, er])
                
    return coordinates


#---write the coordinates (2D print) to the robot ---------------------------------------------------------
def write_coordinates(coordinates, self):
    
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
    
    for x, y, z, e, er in coordinates:
        
        print(f'--{i}--')
        GlobalState().terminal_text += f'--{i}--'
        
        
        # Check exit_program.value instead of exit_program
        if GlobalState().exit_program:  
            
            print('BREAK - exitprogram')
            uf.cleanpose(self)
            time.sleep(10)
            break
        i += 1
        #blank line -> skip
        if(x == None and y == None and z == None):
            continue
        #reference so that constant z is managed if z is not specified
        if(z != None):
            non_none_z = z
        if(x != None):
            non_none_x = x
        if(y != None):
            non_none_y = y  
        

        #if er = True, continue with the next line
        if(er == True):
            print('Error was TRUE -> continued')
            continue

        #extrusion information
        if(e != None):
            print(f'extrusion: {e}')
            #time.sleep(1)
            
        
        #if x and y are not specified, move to current position with z offset
        if (x == None and y == None):
            #pose = get_pose()
            
            #print(f'{non_none_x+x_offset}, {non_none_y + y_offset}, {z+z_0+10}')
            uf.commandPose(non_none_x+x_offset, non_none_y + y_offset, z + z_0 + 10 + GlobalState().user_z_offset, 180, 0, -180, self)
            
        elif z == None:
            
            #print(f'{x+x_offset}, {y+y_offset}, {non_none_z+z_0}')
            uf.commandPose(x+x_offset, y+y_offset, non_none_z + z_0 + GlobalState().user_z_offset, 180, 0, -180, self)
            
        #throw exception
        else:
            print("!-!-!-!-!Line skip error!-!-!-!-!")
            
        #wait for the robot to finish the movement (be close to the target)
        while(uf.ReachedPose() != True):
            time.sleep(0.1)
        #self.WaitIdle()
        time.sleep(0.5)
    #-------------------finished print -----------------------------
    uf.endpose(self)

    return


