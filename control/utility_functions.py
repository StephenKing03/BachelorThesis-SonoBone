import mecademicpy.robot as mdr #mechademicpy API import (see Github documentation)
import time #for time.sleep()
from globals import RobotStats
from globals import GlobalState
import stepper_control as sc
import math

import threading


#---set the speed of the robot in mm/s---------------------------------------------------------
def adjust_speed(speed_p, self = mdr.Robot()):
    self.SendCustomCommand(f'SetJointVelLimit({speed_p * RobotStats().joint_vel_limit/100/2 * 0.5})')
    print(f'LinVel set to {speed_p} %')
    return

#---get real time cartesian position of the robot as an array [x,y,z,alpha,beta,gamma]-------------------------------------------
def GetPose(self = mdr.Robot()):

    rtdata = self.GetRobotRtData()
    #print(rtdata)
    pose = rtdata.rt_cart_pos.data
    #print(f'Pos:{pose}\n')
    
    
    return pose

#probably does not work? - test before use
def GetTargetPose(self = mdr.Robot()):
    

    rtdata = self.GetRobotRtData()
    targetpose = rtdata.rt_target_cart_pos.data

    return targetpose

def ReachedPose(self = mdr.Robot(), target = [0,0,0,0,0,0]):

    pose = GetPose(self)
    distance =  0
    if (target[0] != None):
        distance +=(pose[0]-target[0])**2
    if (target[1] != None):
        distance += (pose[1]-target[1])**2 
    if (target[2] != None):
         (pose[2]-target[2])**2

    distance = distance**0.5

    if(distance < GlobalState().threshold):
        return True
    else:
        #print(" DISTANCE = " + str(distance))
        #print("not reached:" + str(GetPose(GlobalState().msb)) + "  >>>>> " + str(target))
        return False

def WaitReachedPose(target = [0,0,0,0,0,0]):
    #with GlobalState().msb.FileLogger(0.001, fields =['CartPos', 'TargetCartPos']):
    while (not ReachedPose(GlobalState().msb, target) and GlobalState().printing_state != 5):
        time.sleep(0.1)
    GlobalState().semaphore -=1
    #print("--------------------REACHED POSE-------------------")
    return




#---get real time  joint position of the robot as an array [j1,j2,j3,j4,j5,j6]-------------------------------------------
def GetJoints(self = mdr.Robot()):
    j = [None] * 5

    rtdata = self.GetRobotRtData()
    joints = rtdata.rt_joint_pos.data

    return joints
def pause_motion(self = mdr.Robot()):

    return

def resume_motion(self = mdr.Robot()):


    return



#---move the robot in z direction by hop value at current (up=1: up, up=-1: down), hop in [mm] ---------------------------------------------------------
def z_hop(up=-1, hop=10, self = mdr.Robot()):
    
    pose = GetPose(self)

    #extract z value - modify with extra parameters
    z = pose[2]

    #modify z value by hop
    
    #send new pose with modified z value
    self.SendCustomCommand(f'MoveLin({pose[0]},{pose[1]},{z + hop},{pose[3]},{pose[4]},{pose[5]})')
    print(f'z_hop by {up* hop} mm done')

    return

#--check if the given coordinates are within the limits of the buildspace ---------------------------------------------------------
def checklimits(x, y, z, self = mdr.Robot()):
    #check x limits
    if(x > RobotStats().max_x): 
        print(f'x out of bounds for {x}')
        GlobalState().terminal_text += f'x out of bounds for x = {x}'
        self.WaitIdle()
        #time.sleep(2)
        return 1
    elif(x < RobotStats().min_x):
        print(f'x out of bounds for {x}')
        GlobalState().terminal_text += f'x out of bounds for x = {x}'
        self.WaitIdle()
        #time.sleep(2)
        return -1
    #check y limits
    if(y > RobotStats().max_y): 
        print(f'y out of bounds for {y}')
        GlobalState().terminal_text += f'y out of bounds for y = {y}'
        self.WaitIdle()
        #time.sleep(2)
        return 2
    elif(y < RobotStats().min_y):
        print(f'y out of bounds for {y}')
        GlobalState().terminal_text += f'y out of bounds for y = {y}'
        self.WaitIdle()
        #time.sleep(2)
        return -2

    #check z limits
    if(z > RobotStats().max_z + GlobalState().user_z_offset ): 
        print(f'z out of bounds for {z}')
        GlobalState().terminal_text += f'z out of bounds for z = {z}'
        self.WaitIdle()
        #time.sleep(2)
        return 3
    elif(z < RobotStats().min_z+ GlobalState().user_z_offset):
        print(f'z out of bounds for {z}')
        GlobalState().terminal_text += f'z out of bounds for z = {z}'
        self.WaitIdle()
        #time.sleep(2)
        return -3
    return 0


#---move the robot to a predefined position (cleanpose) so that it doesn't obstruct anything---------------------------------------------------------
def cleanpose(self = mdr.Robot()):

    self.MoveJoints(0, -50, 60, 0, 30, 0)

    self.WaitIdle()
    print('cleanpose reached')
    #GlobalState().terminal_text += "Cleanpose reached\n"
    time.sleep(1)

    return

#---move the robot to a predifined position (endpose) so that it is ready to present the print---------------------------------------------------------
def endpose(self = mdr.Robot()):

    self.SendCustomCommand(f'MovePose({150},{0},{65},180,0,-180)')

    self.WaitIdle()
    print('endpose reached')
    #GlobalState().terminal_text += "Endpose reached\n"
    time.sleep(1)

    return

#---move the robot to a predifined position (startpose) so that it is ready to start the print---------------------------------------------------------
def startpose(self = mdr.Robot()):

    self.SendCustomCommand(f'MovePose({150},{0},{RobotStats().min_z + 15},180,0,-180)')

    self.WaitIdle()
    print('startpose reached')
    #GlobalState().terminal_text += "Startpose reached\n"
    time.sleep(1.5)

    return

def callibrationpose(self = mdr.Robot()):

    self.WaitIdle()

    #commandPose((RobotStats().min_x + RobotStats().max_x)/2, 0, RobotStats().min_z + GlobalState().user_z_offset + 10, 180, 0, -180)
    self.SendCustomCommand(f'MovePose({(RobotStats().min_x + RobotStats().max_x)/2}, 0, {RobotStats().min_z + GlobalState().user_z_offset + 10}, 180, 0, -180)')
    
    print("calibrationpose reached")

    

    return

#---single command to deactivate the robot and disconnect it--------------------------------------------------------
def deactivation_sequence(self = mdr.Robot()):

    #ToDo: add deactivation sequence
    

    return

def reset():

    msb = GlobalState().msb
    msb.ResetError()
    msb.ClearMotion()
    msb.SendCustomCommand('ResetError()')
    msb.SendCustomCommand('ResumeMotion()')
    msb.SendCustomCommand(f'SetJointVelLimit({RobotStats().start_joint_vel_limit})')

    return


def init_sequence():

    #connect to robot if the robot is not connected already (e.g. from reset)
    if(GlobalState().msb == None):
        try:    
            GlobalState().msb = mdr.Robot() #msb = MegaSonoBot # instance of the robot class
            GlobalState().msb.Connect(address='192.168.0.100') #using IP address of the robot and Port 10000 to control
            
            GlobalState().msb.ActivateRobot() #same as in the webinterface: activate Robot
            GlobalState().msb.ResetError()
            GlobalState().msb.Home() #Home the robot
            GlobalState().msb.ResetError()
        except:
            print("Could not connect to robot")
            return

    if(GlobalState().arduino_port == None):
       #activate steppers
        sc.init_steppers()
        sc.wait_init()
        
    

        
    msb = GlobalState().msb
    #setup robot arm
    GlobalState().msb.ResetError()
    GlobalState().msb.Home() #Home the robot
    msb.ResetError()
    msb.SendCustomCommand(f'SetJointVelLimit({RobotStats().max_linvel})')
    msb.SendCustomCommand("SetRealTimeMonitoring('cartpos')") #start logging position
    msb.SendCustomCommand('ResetError()')
    msb.SendCustomCommand('ResumeMotion()')
    msb.SendCustomCommand(f'SetJointVelLimit({RobotStats().start_joint_vel_limit})')
    msb.SendCustomCommand(f'SetCartLinVel({RobotStats().max_linvel})')
    msb.SendCustomCommand(f'SetCartAcc({RobotStats().max_acc}')
    msb.SendCustomCommand('SetBlending(70)')
    #Set tooltip reference frame to 160 in front of the end of robot arm
    msb.SendCustomCommand(f'SetTrf({RobotStats().tooloffset_x},{RobotStats().tooloffset_y},{RobotStats().tooloffset_z},{RobotStats().tooloffset_alpha},{RobotStats().tooloffset_beta},{RobotStats().tooloffset_gamma})')
    #setpayload!!!!!--------------------------------
    msb.WaitIdle()

    
    
    #send info text
    GlobalState().msb.WaitIdle()
    time.sleep(1)
    #wait for the initialization to finish
    GlobalState().msb.WaitIdle()

    #set the robot to cleanpose
    cleanpose(GlobalState().msb)
    GlobalState().msb.WaitIdle()



    GlobalState().printing_state = 1 #1 = ready to print
    GlobalState().confirmed = True

    GlobalState().terminal_text += "Robot activated and ready to go!"

    return

def clean_motion(self = mdr.Robot()):

    self.sendCustomCommand("ClearMotion()")
    GlobalState().terminal_text += "Cleared motion queue "

'''depracated'''
def exit_print():

    print('BREAK - exitprogram')
    GlobalState().terminal_text += "-----------BREAK - Print Process Stopped--------------"
    cleanpose(GlobalState().msb)
    time.sleep(3)
    return

#---move the robot to specified position with out of bounds check---------------------------------------------------------
def commandPose(x,y,z,alpha,beta,gamma, self = mdr.Robot()):

    error_code = checklimits(x,y,z,self)
    #check if the pose is within the limits
    if(error_code != 0):
        print(f'Out of bounds detected -> override')
        #GlobalState().terminal_text += "out of bounds\n"

        if(error_code == 1):
            x = RobotStats().max_x
        elif(error_code  == -1):
            x = RobotStats().min_x

        if(error_code  == 2):
            y = RobotStats().max_y
        elif(error_code  == -2):
            y = RobotStats().max_z

        if(error_code  == 3):
            z = RobotStats().max_z + GlobalState().user_z_offset
        elif(error_code  == -3):
            z = RobotStats().min_z+ GlobalState().user_z_offset
    
    GlobalState().msb.SendCustomCommand(f'MovePose({x},{y},{z},{alpha},{beta},{gamma})')

    return

def commandPose5d(x,y,z,alpha,beta,gamma, self = mdr.Robot()):

    #check if the pose is within the limits
    if(z > RobotStats().max_z + GlobalState().user_z_offset ): 
        print(f'z out of bounds for {z}')
        GlobalState().terminal_text += f'z out of bounds for z = {z}'
        z = RobotStats().max_z + GlobalState().user_z_offset

        
    elif(z < RobotStats().min_z+ GlobalState().user_z_offset):
        print(f'z out of bounds for {z}')
        GlobalState().terminal_text += f'z out of bounds for z = {z}'
        z = RobotStats().min_z + GlobalState().user_z_offset
    
    GlobalState().msb.SendCustomCommand(f'MovePose({x},{y},{z},{alpha},{beta},{gamma})')
    return

    
def check_round_bounds(x,y):

    r = math.sqrt(x**2 + y**2)
    if r > RobotStats().diameter/2:
        GlobalState().terminal_text += "\nDiameter of the print is too large for r = " + str(r)+ " \n" + "It must be within r = " + str(RobotStats().diameter /2) 
        return True

    return False
    