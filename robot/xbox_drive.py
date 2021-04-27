import xbox

class JoystickValue:
    def __init__(self, name):
        self.x = 0
        self.y = 0
        self.name = name

    def update(self, x, y):
        # exponential moving average to reduce brownout
        self.x = (100 * x + self.x) / 2 if x != 0 or abs(self.x) > 0.1 else 0
        self.y = (100 * y + self.y) / 2 if y != 0 or abs(self.y) > 0.1 else 0
    
    def __str__(self):
        return f"JoystickValue<{self.name}>: ({self.x}, {self.y})"

    def __repr__(self):
        return self.__str__()

class XboxController:
    def __init__(self):
        self.motor_xy = JoystickValue("Motors")
        self.td_xy = JoystickValue("TrenchDigger")
        self.joy = xbox.Joystick()
    
    def read_controller(self):
        # Left Joystick: Arcade Drive motor control
        mx, my = self.joy.leftStick()
        self.motor_xy.update(mx, my)

        tx, ty = self.joy.rightStick()
        self.td_xy.update(tx, ty)
