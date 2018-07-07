from gpiozero import CompositeDevice, DigitalOutputDevice, PWMOutputDevice, AngularServo
from gpiozero.exc import GPIOPinMissing
from gpiozero.mixins import SourceMixin
import time


class TwoWayMotor(SourceMixin, CompositeDevice):

    def __init__(self, forward=None, backward=None, enable=None):
        if not all(p is not None for p in [forward, backward, enable]):
            raise GPIOPinMissing(
                'all pins must be provided'
            )
        super(TwoWayMotor, self).__init__(
                forward_device=DigitalOutputDevice(forward),
                backward_device=DigitalOutputDevice(backward),
                enable_device=PWMOutputDevice(enable),
                _order=('forward_device', 'backward_device', 'enable_device'))

    def forward(self, speed=1):
        self.forward_device.on()
        self.backward_device.off()
        self.enable_device.value = speed

    def backward(self, speed=1):
        self.forward_device.off()
        self.backward_device.on()
        self.enable_device.value = speed

    def brake(self, speed=1):
        self.forward_device.off()
        self.backward_device.off()
        self.enable_device.value = speed

    def stop(self):
        self.forward_device.off()
        self.backward_device.off()
        self.enable_device.off()


class FourWayMotor(SourceMixin, CompositeDevice):
    def __init__(self, forward=None, backward=None, drivetrain=None, steering=None):
        if not all(p is not None for p in [forward, backward, drivetrain, steering]):
            raise GPIOPinMissing(
                'all pins must be provided'
            )
        super(FourWayMotor, self).__init__(
                drivetrain_device=TwoWayMotor(forward, backward, drivetrain),
                steering_device=AngularServo(steering, min_angle=-60, max_angle=60, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000),
                _order=('drivetrain_device', 'steering_device'))

    def forward(self, speed=1):
        self.drivetrain_device.forward(speed)

    def backward(self, speed=1):
        self.drivetrain_device.backward(speed)

    def brake(self, speed=1):
        self.drivetrain_device.brake(speed)

    def stop(self):
        self.drivetrain_device.stop()

    def turn_left(self, speed=1):
        print(speed * self.steering_device.min_angle)
        self.steering_device.angle = 0.99 * speed * self.steering_device.min_angle

    def turn_right(self, speed=1):
        self.steering_device.angle = 0.99 * speed * self.steering_device.max_angle

    def go_straight(self):
        self.steering_device.angle = 0

    def off(self):
        self.drivetrain_device.stop()
        self.steering_device.angle = None

    def stop_steering(self):
        self.steering_device.angle = None


def default_motor():
    # From http://fritzing.org/projects/raspberry-pi-dual-dc-motor
    return FourWayMotor(27, 22, 17, 2)

