import mecademicpy.robot as mdr #mechademicpy API import (see Github documentation)
import time #for time.sleep()
from main_control import robot_stats


#---get real time cartesian position of the robot as an array [x,y,z,alpha,beta,gamma]-------------------------------------------
def GetPose(self = mdr.Robot()):
    p = [None] * 5
    #pose = self.SendCustomCommand(self,'GetRtCartPos()',p[1],None)
    rtdata = self.GetRobotRtData()
    pose = rtdata.rt_cart_pos.data
    #pose = pose_s.strip('[]').split(',')
    #target = self.GetRtTargetCartPos()
    #pose = self.GetRtCartPos()
    #print(f'Target:{target}\n')
    #print(f'Pos:{pose}\n')

    #manipulate so that pose is an array
    return pose


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
    if(x > robot_stats.max_x or x < robot_stats.min_x): #check x limits
        print(f'x out of bounds in iteration {iteration} for {x}')
        self.WaitIdle()
        time.sleep(2)
        return 1
    if(y > robot_stats.max_y or y < robot_stats.min_y): #check y limits
        print(f'y out of bounds in iteration {iteration} for {y}')
        self.WaitIdle()
        time.sleep(2)
        return 2
    if(z > robot_stats.max_y or z < 0): #check z limits
        print(f'z out of bounds in iteration {iteration} for {z}')
        self.WaitIdle()
        time.sleep(2)
        return 3
    return 0


#---move the robot to a predefined position (cleanpose) so that it doesn't obstruct anything---------------------------------------------------------
def cleanpose(self = mdr.Robot()):

    robot.MoveJoints(0, -60, 60, 0, 0, 0)

    robot.WaitIdle()
    print('cleanpose reached')
    time.sleep(1)

    return

def endpose(self = mdr.Robot()):

    msb.SendCustomCommand(f'MovePose({150},{0},{65+30},180,0,-180)')

    robot.WaitIdle()
    print('endpose reached')
    time.sleep(1)

    return

#single activation command
def activationsequence():

    msb = mdr.Robot() #msb = MegaSonoBot # instance of the robot class
    msb.Connect(address='192.168.0.100') #using IP address of the robot and Port 10000 to control
    msb.ActivateRobot() #same as in the webinterface: activate Robot
    msb.Home() #Home the robot
    msb.ClearMotion()
    msb.SendCustomCommand('ResetError()')
    msb.SendCustomCommand('ResumeMotion()')
    msb.SendCustomCommand(f'SetJointVelLimit({robot_stats.joint_vel_limit})')
    msb.SendCustomCommand(f'SetCartLinVel({robot_stats.max_linvel})')
    msb.SendCustomCommand('SetBlending(60)')

    #setpayload!!!!!--------------------------------

    #Set tooltip reference frame to 160 in front of the end of robot arm
    msb.SendCustomCommand('SetTrf(0,0,160,0,0,0)')

    #send info text
    msb.WaitIdle()
    print('Robot activated and ready to go!')
    time.sleep(1)


    return msb

def deactivationsequence():

    msb.WaitIdle()
    msb.DeactivateRobot()
    msb.Disconnect()

    return
    