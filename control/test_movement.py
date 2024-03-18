import math
import utility_functions as uf


def print_square(x_length, y_length, nozzle_size, x_offset, y_offset, self):
    z = 65.5
    self.SendCustomCommand(f'MovePose({x_offset},{-y_length/2+y_offset},{z+10},180,0,-180)')
    time.sleep(10)

    for x in range(0, x_length, nozzle_size):
        self.SendCustomCommand(f'MoveLin({x+x_offset}, {-y_length/2+y_offset}, {z}, 180, 0, -180)')
        self.SendCustomCommand(f'MoveLin({x+x_offset+nozzle_size/2}, {-y_length/2+y_offset}, {z}, 180, 0, -180)')
        self.SendCustomCommand(f'MoveLin({x+x_offset+nozzle_size/2}, {y_length/2+y_offset}, {z}, 180, 0, -180)')
        self.WaitIdle()
    uf.z_hop(1, self)

    uf.cleanpose(self)
    
    return
        

def print_smiley(diameter, center_x, nozzle_size):
    z = 150
    offset_mouth = diameter/10
    angle_mouth = 60
    eye_y_of
    
    
    fset = diameter/10
    eye_x_length= diameter/5
    
    
    #travel to outside circle
    
    msb.SendCustomCommand(f'MoveLin({center_x + diameter/2, center_x}, {z+10}, 180, 0, -180)')
    uf.z_hop(-1, msb)
    #draw outside circle
    for angle in range(0, 360, nozzle_size/diameter*2/(math.pi*2)*360):
        x = center_x + diameter/2 * math.cos(math.radians(angle))
        y = center_x + diameter/2 * math.sin(math.radians(angle))
        msb.SendCustomCommand(f'MoveLin({x}, {y}, {z}, 180, 0, -180)')
        #msb.SendCustomCommand(f'MoveLin({x}, {y + diameter}, {z}, 180, 0, -180)')
        msb.waitIdle()
        

    #travel to mouth
    uf.z_hop(1,msb)
    
    x = center_x + diameter/2 * math.cos(math.radians(-90-angle_mouth/2))
    y = center_x + diameter/2 * math.sin(math.radians(-90-angle_mouth/2))
    msb.SendCustomCommand(f'MoveLin({x}, {y}, {z+10}, 180, 0, -180)')
    
    #draw mouth
    uf.z_hop(-1,msb)
    for angle in range(-90-angle_mouth/2, -90+angle_mouth/2, nozzle_size/diameter*2/(math.pi*2)*360):
        x = center_x + diameter/2 * math.cos(math.radians(angle))
        y = center_x + diameter/2 * math.sin(math.radians(angle))
        msb.SendCustomCommand(f'MoveLin({x}, {y}, {z}, 180, 0, -180)')
        #msb.SendCustomCommand(f'MoveLin({x}, {y + diameter}, {z}, 180, 0, -180)')
        msb.waitIdle()
        

    #travel to eye1
    uf.z_hop(1,msb)
    msb.SendCustomCommand(f'MoveLin({center_x }, {center_x + eye_y_offset}, {z+10}, 180, 0, -180)')
    uf.z_hop(-1,msb)
    #draw eye1
    msb.SendCustomCommand(f'MoveLin({center_x+eye_x_length}, {center_x + eye_y_offset}, {z}, 180, 0, -180)')

    #travel to eye2
    uf.z_hop(1,msb)
    msb.SendCustomCommand(f'MoveLin({center_x }, {center_x - eye_y_offset}, {z+10}, 180, 0, -180)')
    uf.z_hop(-1,msb)
    #draw eye2
    msb.SendCustomCommand(f'MoveLin({center_x+eye_x_length}, {center_x - eye_y_offset}, {z}, 180, 0, -180)')
    uf.z_hop(1,msb)

    uf.cleanpose()

    return


