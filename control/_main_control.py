import mecademicpy.robot as mdr #mechademicpy API import (see Github documentation)
import time #for time.sleep()
import utility_functions as uf #import utility functions
import gcode_translator as gt #import gcode translator
from robot_stats import robot_stats

#initiate robot
stats = robot_stats()
msb = uf.activationsequence()

#set initial position
uf.cleanpose(msb)

#------------load file ---------------------
file_path = r"C:\Users\steph\OneDrive\_Studium\_Semester 6 (FS2024)\Bachelor Thesis\CODEBASE\BachelorThesis_SonoBone\gcode\Bone2.gcode"

#-----------print 2D file-----------------------
gt.write_coordinates(gt.extract_coordinates(file_path), msb)



