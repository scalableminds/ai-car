from gpiozero import CompositeDevice, DigitalOutputDevice, PWMOutputDevice
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
    def __init__(self, forward=None, backward=None, drivetrain=None, left=None, right=None, steering=None):
        if not all(p is not None for p in [forward, backward, drivetrain, left, right, steering]):
            raise GPIOPinMissing(
                'all pins must be provided'
            )
        super(FourWayMotor, self).__init__(
                drivetrain_device=TwoWayMotor(forward, backward, drivetrain),
                steering_device=TwoWayMotor(left, right, steering),
                _order=('drivetrain_device', 'steering_device'))


    def forward(self, speed=1):
        self.drivetrain_device.forward(speed)

    def backward(self, speed=1):
        self.drivetrain_device.backward(speed)

    def brake(self, speed=1):
        self.drivetrain_device.brake(speed)

    def stop(self):
        self.drivetrain_device.stop()

    def turn_left(self):
        self.steering_device.forward()

    def turn_right(self):
        self.steering_device.backward()

    def go_straight(self):
        self.steering_device.stop()

    def off(self):
        self.drivetrain_device.stop()
        self.steering_device.stop()


def default_motor():
    # From http://fritzing.org/projects/raspberry-pi-dual-dc-motor
    return FourWayMotor(27, 22, 17, 24, 4, 23)

