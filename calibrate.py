from gpiozero import AngularServo
from time import sleep
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("mid", help="Pulse to steer middle. Unit=milliseconds. Should be roughly between 1ms and 2ms", type=float)
parser.add_argument("range", help="Pulse offset of mid to steer left or right (plus or minus respectively). Unit=milliseconds. Should be between 0ms and 1ms.", type=float)
args = parser.parse_args()

minPW = (args.mid - args.range) / 1000
maxPW = (args.mid + args.range) / 1000

servo = AngularServo(2, min_angle=-60, max_angle=60, min_pulse_width=minPW, max_pulse_width=maxPW)
servo.angle = 0

for i in range(3):
  sleep(1)
  servo.angle = -60
  print('LEFT')
  sleep(1)
  servo.angle = 0
  print('MID')
  sleep(1)
  servo.angle = 60
  print('RIGHT')
  sleep(1)
  servo.angle = 0
  print('MID')

