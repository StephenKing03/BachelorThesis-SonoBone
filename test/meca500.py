class Meca500:
    
    """control a Meca500 robot with Python"""

    def __init__(self, ipAddress):

        import socket
        PORT = 10000  # the port used by the server
        
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((ipAddress, PORT))
        self.s.settimeout(3.0)
        self.s.recv(1024)

    def __del__(self):

        import socket
        
        self.s.shutdown(socket.SHUT_RDWR)
        self.s.close()

    def sendToRobot(self, command):

        b = bytes(command+"\n", 'utf-8')
        self.s.sendall(b)
        data = self.s.recv(1024)
        return data

    def activate(self):
    
        str = self.sendToRobot("ActivateRobot()")
        return str

    def deactivate(self):
    
        str = self.sendToRobot("DeactivateRobot()")
        return str

    def reset(self):
    
        str = self.sendToRobot("ResetError()")
        return str

    def home(self):
    
        str = self.sendToRobot("Home()")
        return str

    def setJointVelocity(self, v):
    
        str = self.sendToRobot(f"SetJointVel({v:.3f})")
        return str

    def moveJoints(self, theta):

        str = self.sendToRobot(f"MoveJoints({theta[0]:.3f},{theta[1]:.3f},{theta[2]:.3f},{theta[3]:.3f},{theta[4]:.3f},{theta[5]:.3f})")
        return str

#---------testing
    
    robot = Meca500("192.168.0.100")
    robot.activate()
    robot.home()
    response = robot.sendToRobot(f"MoveJoints({45:.3f},{45:.3f},{0:.3f},{0:.3f},{0:.3f},{0:.3f})")

    # Print the response from the robots
    
    print(response)


    robot.deactivate()