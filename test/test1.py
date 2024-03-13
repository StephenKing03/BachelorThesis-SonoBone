
import mecademicpy.robot as mdr
import time

robot = mdr.Robot()
robot.Connect(address='192.168.0.100')
robot.ActivateRobot()
robot.Home()

robot.SendCustomCommand('SetTrf(0,0,155,0,0,0)')

robot.MoveJoints(-45, 0, 0, 0, 0, 0)
time.sleep(3)
robot.MoveJoints(0, -60, 60, 0, 0, 0)
time.sleep(3)
robot.SendCustomCommand('MoveLin(150,0,100,180,0,-180)')

robot.WaitIdle()
robot.DeactivateRobot()
robot.Disconnect()