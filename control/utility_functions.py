import mecademicpy.robot as mdr #mechademicpy API import (see Github documentation)
import time #for time.sleep()
from globals import RobotStats
from globals import GlobalState

import threading


#---set the speed of the robot in mm/s---------------------------------------------------------
def adjust_speed(speed_p, self = mdr.Robot()):
    self.SendCustomCommand(f'SetJointVelLimit({speed_p * RobotStats().max_linvel/100/2})')
    print(f'LinVel set to {speed_p} %')
    return

#---get real time cartesian position of the robot as an array [x,y,z,alpha,beta,gamma]-------------------------------------------
def GetPose(self = mdr.Robot()):

    rtdata = self.GetRobotRtData()
    print(rtdata)
    pose = rtdata.rt_cart_pos.data
    print(f'Pos:{pose}\n')
    
    
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

#adds target positions to the stack
'''NOT USED AT THE MOMENT'''
def add_target_pose(target = [0,0,0,0,0,0]):

    GlobalState().semaphore += 1
    
    if(GlobalState().target_positions == None):
        GlobalState().target_positions = [target]
        return
    
    elif(len(GlobalState().target_positions) < RobotStats().max_semaphores):
        GlobalState().target_positions.insert(0, target)

    elif(len(GlobalState().target_positions) == RobotStats().max_semaphores):
        GlobalState().terminal_text += "!!!!!!!!!!!!!!!!!! target stack full!!!!!!!!!!!!\n"

    else:
        GlobalState().terminal_text += "!!!!!!!!!!!!!!!!!! DIFFERENT target stack error!!!!!!!!!!!!\n"
    return

#continuously running thread that checks the current target pose of the robot to reduce semaphores
'''NOT USED AT THE MOMENT'''
def check_target_pose():
    start_time = time.time()
    paused_time = 0
    pause_time_start = 0
    while True:

            if(GlobalState().printing_state == 5): #exit program
                break

            while(GlobalState().semaphore == 0): #wait for new target
                time.sleep(0.01)


            start_time = time.time() #reset timer
            while( not ReachedPose(GlobalState().msb, GlobalState().target_positions[RobotStats().max_semaphores-1])):
                if(GlobalState().printing_state == 5): #exit program
                    break
                if (GlobalState().printing_state == 3): #paused
                    pause_time_start = time.time()
                    while(GlobalState().printing_state == 3):
                        time.sleep(0.1)
                    paused_time += time.time() - pause_time_start

                if(time.time() - start_time - paused_time > 5): #timeout
                    GlobalState().terminal_text += "!!!!!!!!!!!!!!!!!!Semaphore reduced - timeout!!!!!!!!!!!!\n"
                    break
                time.sleep(0.01)
            GlobalState().target_positions.pop()
            GlobalState().semaphore -= 1
        

    return
#---get real time  joint position of the robot as an array [j1,j2,j3,j4,j5,j6]-------------------------------------------
def GetJoints(self = mdr.Robot()):
    j = [None] * 5

    rtdata = self.GetRobotRtData()
    joints = rtdata.rt_joint_pos.data

    return joints

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

    self.MoveJoints(0, -60, 60, 0, 0, 0)

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
def deactivationsequence(self = mdr.Robot()):

    #ToDo: add deactivation sequence
    

    return

def clean_motion(self = mdr.Robot()):

    self.sendCustomCommand("ClearMotion()")
    GlobalState().terminal_text += "Cleared motion queue "

'''depracated'''
def exit_print():

    print('BREAK - exitprogram')
    GlobalState().terminal_text += "-----------BREAK - Print Process Stopped--------------"
    uf.cleanpose(self)
    time.sleep(3)
    return

#---move the robot to specified position with out of bounds check---------------------------------------------------------
def commandPose(x,y,z,alpha,beta,gamma, self = mdr.Robot()):

    #check if the pose is within the limits
    if(checklimits(x, y, z, self) != 0):
        print(f'Out of bounds detected -> override')
        #GlobalState().terminal_text += "out of bounds\n"

        if(checklimits(x, y, z, self) == 1):
            x = RobotStats().max_x
        elif(checklimits(x, y, z, self)  == -1):
            x = RobotStats().min_x

        if(checklimits(x, y, z, self)  == 2):
            y = RobotStats().max_y
        elif(checklimits(x, y, z, self)  == -2):
            y = RobotStats().max_z

        if(checklimits(x, y, z, self)  == 3):
            z = RobotStats().max_z + GlobalState().user_z_offset
        elif(checklimits(x, y, z, self)  == -3):
            z = RobotStats().min_z+ GlobalState().user_z_offset
    

    #print(f'alpha: {alpha}, beta: {beta}, gamma: {gamma}')
   
    
    '''
    alpha += alpha +180

    if(alpha >180):
        alpha -= 360

     #----------disclaimer ------
    
    if(alpha <180-20):
        print(f'alpha out of bounds for {alpha}')
        alpha = 180-20
        
    if(alpha >-180+20):
        print(f'alpha out of bounds for {alpha}')       
        alpha = -180+20
    '''
    GlobalState().msb.SendCustomCommand(f'MovePose({x},{y},{z},{alpha},{beta},{gamma})')
    #add_target_pose([x,y,z,alpha,beta,gamma])
    #self.MovePose({x},{y},{z},{alpha},{beta},{gamma})
    #self.WaitIdle()
    print(f'Pose entered: {x},{y},{z},{alpha},{beta},{gamma}')

    #GlobalState().terminal_text += "Pose:" + str(round(x,4)) + "," + str(round(y,4)) + "," + str(round(z,4)) + "," + str(round(alpha,4)) + "," + str(round(beta,4)) + ","  + str(round(gamma,4)) + ""
    
    #time.sleep(0.3)
    

    return
    