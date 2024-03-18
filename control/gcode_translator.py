import math
import time #for time.sleep()

def extract_coordinates(file_path):
    coordinates = []
    with open(file_path, 'r') as file:
        i = 0
        for line in file:
            if i <44:
                i+=1
                continue
            if line.startswith('G0') or line.startswith('G1'):
                # Extracting X, Y, and Z coordinates
                #print(f'---------------------------------{line}')
                x = None
                y = None
                z = None
                for command in line.split():
                    if command.startswith('X'):
                        x = float(command[1:])
                    elif command.startswith('Y'):
                        y = float(command[1:])
                    elif command.startswith('Z'):
                        try:
                            z = float(command[1:])
                        except:
                            if command.startswith('E-2'):
                                z = 100
                            else:
                                z = -100
                coordinates.append([x, y, z])
                
    return coordinates

def write_coordinates(coordinates, self):
    z_std = 63-140.8 + 10.5 +0.45
    x_offset = 80
    y_offset = -110
    non_none_z = 100
    non_none_x = 100
    non_none_y = 0
    i = 0
    
    for x, y, z in coordinates:
        print(f'--{i}--')
        i +=1
        #blank line -> skip
        if(x == None and y == None and z == None):
            continue
        #reference so that constant z is managed if z is not specified
        if(z != None and z != 100 and z != -100):
            non_none_z = z
        if(x != None):
            non_none_x = x
        if(y != None):
            non_none_y = y  
        

        #if z = 100, stop
        if(z == 100 or z == -100):
            print('special case reached -> continued')

        elif(x != None and x + x_offset <= 100):
            print('X-crash detected')
            continue
            
        
        #if x and y are not specified, move to current position with z offset
        elif x == None and y == None:
            #pose = get_pose()
            
            print(f'{non_none_x+x_offset}, {non_none_y + y_offset}, {z+z_std+10}')
            self.SendCustomCommand(f'MoveLin({non_none_x+x_offset}, {non_none_y + y_offset}, {z+z_std+10}, {180}, {0}, {-180})')
            
        elif z == None:
            
            print(f'{x+x_offset}, {y+y_offset}, {non_none_z+z_std}')
            self.SendCustomCommand(f'MoveLin({x+x_offset}, {y+y_offset}, {non_none_z+z_std}, {180}, {0}, {-180})')
            
        #throw exception
        else:
            print("!ALL ZEROES")
        
        #self.WaitIdle()
        #time.sleep(0.5)

    return

#file_path = r"C:\Users\steph\OneDrive\_Studium\_Semester 6 (FS2024)\Bachelor Thesis\CODEBASE\BachelorThesis-SonoBone\gcode\ARSL_am.gcode"

# Extract coordinates
#coordinates = extract_coordinates(file_path)
#for i in range(0, len(coordinates)):
#    print(f'{i}: {coordinates[i]}\n')
    
