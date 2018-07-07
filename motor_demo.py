import time
from writers.motor import default_motor

motor = default_motor()

while True:
    print("Loop")
    motor.forward(0.6)
    motor.turn_left()
    time.sleep(1)

    motor.stop()
    time.sleep(0.2)

    motor.backward(0.6)
    motor.turn_right()
    time.sleep(1)

    motor.stop()
    motor.go_straight()
    time.sleep(0.2)

