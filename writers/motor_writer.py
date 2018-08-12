from writers.motor import default_motor
from writers.writer import Writer


class MotorWriter(Writer):
    def __init__(self, frequency=100, speed=0.6):
        self.frequency = frequency
        self.speed = speed

    def __enter__(self):
        self.motor = default_motor()
        self.motor.drivetrain_device.enable_device.frequency = self.frequency
        return self

    def __exit__(self, exit_type, value, traceback):
        self.motor.off()
        del self.motor

    def write(self, data):
        if data is None:
            return
        keys = data

        if "LEFT" in keys:
            self.motor.turn_left()
        elif "RIGHT" in keys:
            self.motor.turn_right()
        else:
            self.motor.go_straight()

        if "BRAKE" in keys:
            self.motor.brake()
        elif "UP" in keys:
            self.motor.forward(speed=self.speed)
        elif "DOWN" in keys:
            self.motor.backward(speed=self.speed)
        else:
            self.motor.stop()

    def write_num(self, x, y):
        if x > 0:
            self.motor.turn_left(x)
        elif x < 0:
            self.motor.turn_right(-x)
        else:
            self.motor.go_straight()

        if y > 0:
            self.motor.forward(speed=self.speed/y)
        elif y < 0:
            self.motor.backward(speed=-self.speed/y)
        else:
            self.motor.stop()

