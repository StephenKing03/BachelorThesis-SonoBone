import mecademicpy.robot as mdr #mechademicpy API import (see Github documentation)
import time #for time.sleep()
import utility_functions as uf #import utility functions
import gcode_translator as gt

from test_movement import print_smiley, print_square

printbed_z = -100


#initial position

time.sleep(2)



#------------load ---------------------
#print_smiley(50,150,2)
#uf.z_hop(1,10,msb)
print_square(90,150,1,120,0, msb)
#draw asrl am logo
# Specify the path to your .gcode file
file_path = r"C:\Users\steph\OneDrive\_Studium\_Semester 6 (FS2024)\Bachelor Thesis\CODEBASE\BachelorThesis_SonoBone\gcode\Bone2.gcode"
# Extract coordinates
coordinates = gt.extract_coordinates(file_path)

# Write the coordinates
#gt.write_coordinates(coordinates, msb)
# Print the coordinates
#for coordinate in coordinates:
 #   print(coordinate)



# ----- present print ----
msb.SendCustomCommand(f'MovePose({150},{0},{65+20},180,0,-180)')




#finish the program
msb.WaitIdle()
msb.DeactivateRobot()
msb.Disconnect()