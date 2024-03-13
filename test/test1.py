
import mecademicpy.robot as mdr
import time

robot = mdr.Robot()
robot.Connect(address='192.168.0.100')
robot.ActivateRobot()
robot.Home()

robot.MoveJoints(-45, 0, 0, 0, 0, 0)
time.sleep(5)
robot.MoveJoints(0, -60, 60, 0, 0, 0)

robot.WaitIdle()
robot.DeactivateRobot()
robot.Disconnect()