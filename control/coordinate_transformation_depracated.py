import numpy as np


def rad_to_deg(rad):
    return rad * 180 / np.pi

def rotation_around_z(pre, theta):
    return np.array([[np.cos(theta), -np.sin(theta), 0],
                     [np.sin(theta), np.cos(theta), 0],
                     [0, 0, 1]]) @ pre 

def transform_rotating_base(coordinate):

    r = coordinate[3:6]
    p_pre = coordinate[0:3]
    #print("r: " + str(r))
    #print("p: " + str(p_pre))

    #get angle phi from v to z-axis
    phi = np.arccos(r[2] / np.linalg.norm(r))

    #get angle theta from v projected into the xy-plane to y-axis
    theta = np.arccos(r[1] / (np.sin(phi) * np.linalg.norm(r)))


    #transform coordinates from before p_pre to p_post
    p_post = rotation_around_z(p_pre, theta)

    
    return [p_post[0], p_post[1], p_post[2], rad_to_deg(theta), rad_to_deg(phi)]


def shift_to_middle(coordinates):

    min_x = coordinates[0][0]
    max_x = coordinates[0][0]
    max_y = coordinates[0][1]
    min_y = coordinates[0][1]
    min_z = 0
    max_z = 0

    #get max and min x and y
    for x, y, z, a, b, c, e, er in coordinates:
        if x != None:
            if x > max_x:
                max_x = x
            elif x < min_x:
                min_x = x
        if y != None:
            if y > max_y:
                max_y = y
            elif y < min_y:
                min_y = y
        

        GlobalState().max_z_offset = RobotStats().max_z - max_z


#calculate offset so that the print is centered
    '''           + (half the distance left if evenly spaced)     '''
    x_offset = -min_x  + (max_x - min_x) /2
    '''         (align to the left edge)      + (half the distance left if evenly spaced)      '''
    y_offset = -min_y  + max_y - min_y /2


    return x_offset, y_offset