def GetPose():
    pose = msb.SendCustomCommand(GetRtCartPos())
    #manipulate so that pose is an array
    return pose

def z_hop(up=-1, hop=10):
    
    pose = GetPose()

    #extract z value
    z = pose[2]

    #modify z value by hop
    z+= up*hop
    
    
    #send new pose
    msb.SendCustomCommand(f'MoveLin({pose[0]},{pose[1]},{z},{pose[3]},{pose[4]},{pose[5]})')