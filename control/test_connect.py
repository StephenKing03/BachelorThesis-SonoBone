import mecademicpy.robot as mdr #mechademicpy API import (see Github documentation)
import time #for time.sleep()

from test_movement import print_smiley, print_square

msb = mdr.Robot() #msb = MegaSonoBot # instance of the robot class
msb.Connect(address='192.168.0.100') #using IP address of the robot and Port 10000 to control
msb.ActivateRobot() #same as in the webinterface: activate Robot
msb.Home() #Home the robot

msb.SendCustomCommand('SetTrf(0,0,155,0,0,0)') #Set tooltip reference frame to 155mm in front of the end of robot arm


#load programs
#print_smiley(50,150,2)
print_square(30,100,2,130,0, msb)

#draw asrl am logo

# Specify the path to your .gcode file
#file_path = r"C:\Users\steph\OneDrive\_Studium\_Semester 6 (FS2024)\Bachelor Thesis\CODEBASE\BachelorThesis-SonoBone\gcode\ARSL_am.gcode"

# Extract coordinates
#coordinates = extract_coordinates(file_path)

# Write the coordinates
#write_coordinates(coordinates)
# Print the coordinates
#for coordinate in coordinates:
 #   print(coordinate)




#finish the program
msb.WaitIdle()
msb.DeactivateRobot()
msb.Disconnect()