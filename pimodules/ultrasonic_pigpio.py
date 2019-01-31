import time
import pigpio

def _echo1(gpio, level, tick):
   global _high
   _high = tick

def _echo0(gpio, level, tick):
   global _done, _high, _time
   _time = tick - _high
   _done = True

def readDistance(_trig, _echo):
   global pi, _done, _time
   _done = False
   pi.set_mode(_trig, pigpio.OUTPUT)
   pi.gpio_trigger(_trig,50,1)
   pi.set_mode(_echo, pigpio.INPUT)
   time.sleep(0.0001)
   tim = 0
   while not _done:
      time.sleep(0.001)
      tim = tim+1
      if tim > 50:
         return -1
   return _time/58

pi = pigpio.pi()

if __name__ == "__main__":
   my_echo1 = pi.callback(20, pigpio.RISING_EDGE,  _echo1)
   my_echo0 = pi.callback(20, pigpio.FALLING_EDGE, _echo0)

   while 1:
      print(readDistance(25,20))
      time.sleep(0.05)