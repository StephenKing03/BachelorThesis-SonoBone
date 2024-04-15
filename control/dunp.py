import gui
import threading
import time
import logging
from globals import GlobalState
from globals import RobotStats
import mecademicpy.robot as mdr #mechademicpy API import (see Github documentation)
import utility_functions as uf
import gcode_translator as gt

file_path = r"C:\Users\steph\OneDrive\_Studium\_Semester 6 (FS2024)\Bachelor Thesis\CODEBASE\BachelorThesis_SonoBone\gcode\ecoflex\Sono.gcode"

msb = mdr.Robot() #msb = MegaSonoBot # instance of the robot class
msb.Connect(address='192.168.0.100',enable_synchronous_mode=True) #using IP address of the robot and Port 10000 to control
msb.ActivateRobot() #same as in the webinterface: activate Robot
msb.Home() #Home the robot


#setup robot 
msb.ClearMotion()
msb.SendCustomCommand("SetRealTimeMonitoring('cartpos')") #start logging position
msb.SendCustomCommand('ResetError()')
msb.SendCustomCommand('ResumeMotion()')
msb.SendCustomCommand(f'SetJointVelLimit({RobotStats().joint_vel_limit_start})')
msb.SendCustomCommand(f'SetCartLinVel({RobotStats().max_lin_acc})')
msb.SendCustomCommand(f'SetCartLinVel({RobotStats().max_linvel_start})')
msb.SendCustomCommand(f'SetCartAcc({RobotStats().max_acc}')
msb.SendCustomCommand('SetBlending(40)')

uf.commandPose(150,0,-30,180,0,-180,msb)
uf.commandPose(150,-80,-30,180,0,-180,msb)
uf.commandPose(200,80,-30,180,0,-180,msb)
uf.commandPose(200,-80,-30,180,0,-180,msb)
uf.commandPose(150,-80,-30,180,0,-180,msb)
uf.commandPose(150,80,-30,180,0,-180,msb)

with msb.FileLogger(0.001, fields =['CartPos', 'TargetCartPos']):
    gt.write_coordinates(gt.extract_coordinates(file_path), mdr.Robot())