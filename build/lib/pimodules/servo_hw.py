from time import sleep
import pigpio
from os import system

class CONTROL:
	"""
	This module abstract the action of a typical servo by hardware PWM: 
	1. little step cycle in two opposite direction choices
	2. direct cycle to specific angle
	3. reset to initial angle

	Be careful to set the range to protest your servo.
	"""
	def __init__(self, PIN, STRIDE= 0.01, NOMINAL=1500, RANGE=1000, reset=True):
		self.STRIDE= STRIDE # step magnitude
		self.NOMINAL= NOMINAL  # initial digital cycle/angle
		self.RANGE = RANGE  # range limitation
		self.previous_dc = self.NOMINAL # tracking the previous angle
		self.MAX_DC = self.NOMINAL +  self.RANGE # high limit
		self.MIN_DC = self.NOMINAL -  self.RANGE # low limit
		self.PIN = PIN
		self.start(reset)

	def start(self, reset=True):
		self.pi = pigpio.pi()
		if not self.pi.connected:
			print("starting pigpiod")
			res = system("sudo pigpiod")
			sleep(3)
			if res != 0 :
				print("can't start pigpiod")
				exit()
			self.pi = pigpio.pi()
		if reset:
			self.reset()

	def step_move(self,direction=1.0):
		"""
		Cycle servo a little step.
		This function can only control the direction.

		Limit: servo can't cycle out of the given range.

		:param direction: 1.0 or -1.0
		"""
		dc = self.previous_dc + direction * self.RANGE * self.STRIDE
		if dc > self.MAX_DC or dc < self.MIN_DC:
			print("WARNING!! The servo reached the limit.")
		else:
			self.pi.set_servo_pulsewidth(self.PIN, dc)  
			self.previous_dc = dc


	def direct_move(self, dc, given_time = 1.0):
		"""
		Cycle the servo directly to specific angle.
		The servo works in async with this function.
		Make sure giving the servo some time to move
		before giving it other commands.
		
		Limit: servo can't cycle out of the given range.

		:param dc: digital cycle, can be treat as postion 
		of ther servo
		:param given_time: give servo time to cycle 
		to position

		"""
		if dc > self.MAX_DC:
			print("WARNING!! {} is higher than the high limit {}".format(dc, self.MAX_DC))
			dc = self.MAX_DC
		elif dc < self.MIN_DC:
			print("WARNING!! {} is lower than the low limit {}".format(dc, self.MIN_DC))
			dc = self.MIN_DC
			
		self.pi.set_servo_pulsewidth(self.PIN, dc)
		if given_time > 0.0: sleep(given_time)
		self.previous_dc = dc


	def reset(self):
		"""
		reset to initial angle
		"""
		self.direct_move(self.NOMINAL)

	def stop(self, reset=True):
		"""
		make sure to invoke this function 
		to quit your program elegantly
		"""
		if reset:
			self.reset()
		self.pi.set_servo_pulsewidth(self.PIN, 0)

	def close(self, reset=True):
		self.stop(reset=reset)
		self.pi.stop()

