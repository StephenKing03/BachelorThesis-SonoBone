import math
import time #for time.sleep()
import utility_functions as uf #import utility functions
from main_control import robot_stats

#---extract the coordinates from the gcode file---------------------------------------------------------
def extract_coordinates(file_path):
    coordinates = []
    with open(file_path, 'r') as file:
        i = 0
        for line in file:
            if i <44:
                i+=1
                continue
            if line.startswith('G0') or line.startswith('G1'):
                x = None
                y = None
                z = None
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
                coordinates.append([x, y, z])
                
    return coordinates


#---write the coordinates (2D print) to the robot ---------------------------------------------------------
def write_coordinates(coordinates, self):

    z_0 = robot_stats.min_z
    x_offset = robot_stats.min_x
    y_offset = robot_stats.min_y
    non_none_z = 0
    non_none_x = 0
    non_none_y = 0
    i = 0

    #set reference position:
    uf.startpose(self)
    
    for x, y, z, er in coordinates:
        print(f'--{i}--')
        i +=1
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

        
        if(uf.checklimits(x, y, z, self) == 1):
            x = robot_stats.max_x
        elif(uf.checklimits(x, y, z, self)  == -1):
            x = robot_stats.min_x

        if(uf.checklimits(x, y, z, self)  == 2):
            y = robot_stats.max_y
        elif(uf.checklimits(x, y, z, self)  == -2):
            y = robot_stats.max_z

        if(uf.checklimits(x, y, z, self)  == 3):
            z = robot_stats.max_z
        elif(uf.checklimits(x, y, z, self)  == -3):
            z = robot_stats.min_z
        print(f'Out of bounds detected -> continued')
            
            
        
        #if x and y are not specified, move to current position with z offset
        if (x == None and y == None):
            #pose = get_pose()
            
            print(f'{non_none_x+x_offset}, {non_none_y + y_offset}, {z+z_0+10}')
            uf.commandPose(non_none_x+x_offset, non_none_y + y_offset, z+z_std+10, 180, 0, -180)
            
        elif z == None:
            
            print(f'{x+x_offset}, {y+y_offset}, {non_none_z+z_std}')
            uf.commandPose(x+x_offset, y+y_offset, non_none_z+z_0, 180, 0, -180)
            
            
        #throw exception
        else:
            print("BIG ERROR")
        
        #self.WaitIdle()
        #time.sleep(0.5)
    
    uf.endpose(self)

    return


