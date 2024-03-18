import mecademicpy.robot as mdr #mechademicpy API import (see Github documentation)

def GetPose(self = mdr.Robot()):
    p = [None] * 5
    pose = self.SendCustomCommand(self,'GetRtCartPos()',p[1],None)
    #target = self.GetRtTargetCartPos()
    #pose = self.GetRtCartPos()
    #print(f'Target:{target}\n')
    print(f'Pos:{pose}\n')

    #manipulate so that pose is an array
    return pose

def z_hop(up=-1, hop=10, self = mdr.Robot()):
    
    pose = GetPose(self)

    #extract z value
    z = pose[2]

    #modify z value by hop
    z+= up*hop
    
    
    #send new pose
    #self.SendCustomCommand(f'MoveLin({pose[0]},{pose[1]},{z},{pose[3]},{pose[4]},{pose[5]})')

    def cleanpose(self = mdr.Robot()):
        robot.MoveJoints(0, -60, 60, 0, 0, 0)