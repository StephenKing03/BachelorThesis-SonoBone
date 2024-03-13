# control a Meca500 robot with Python

from Meca500 import Meca500

meca = Meca500("192.168.0.100")

meca.activate()
meca.home()

meca.setJointVelocity(50)

meca.moveJoints([0, 0, 0, 0, 0, 0])
meca.moveJoints([45, 0, 0, 0, 0, 0])
meca.moveJoints([45, 30, 30, 0, 30, 0])

meca.moveJoints([45, 0, 0, 0, 0, 0])
meca.moveJoints([0, 0, 0, 0, 0, 0])

meca.deactivate()

del meca
