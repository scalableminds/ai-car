from writers.motor import default_motor
from writers.writer import Writer


class MotorWriter(Writer):
    def __enter__(self):
        self.motor = default_motor()
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

        if "UP" in keys:
            self.motor.forward()
        elif "DOWN" in keys:
            self.motor.backward()
        else:
            self.motor.brake()

        if len(keys) == 0:
            self.motor.stop()

