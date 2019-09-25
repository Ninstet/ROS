#!/usr/bin/python

import time
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

class wall_hugger():

	def __init__(self, left=0.0, front=0.0, right=0.0, distance=1.0, threshold=0.3):
		self.left = left
		self.front = front
		self.right = right
		self.distance = distance
		self.threshold = threshold

		rospy.init_node('wall_hugger', anonymous=True)
		rate = rospy.Rate(5)

		velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
		scan_subscriber = rospy.Subscriber('/front/scan', LaserScan, self.callback)

		vel_msg = Twist()

		while not rospy.is_shutdown():

			vel_msg.linear.x = 1
			vel_msg.angular.z = 0

			print(str(self.left - self.distance))

			if self.left - self.distance > self.threshold:
				vel_msg.angular.z = (self.left - self.distance) * 2
			elif self.distance - self.left > self.threshold:
				vel_msg.angular.z = -1 * (self.left - self.threshold) * 2

			velocity_publisher.publish(vel_msg)

			rate.sleep()

	def angle_to_range(self, angle):
		return int((8.0 / 3.0) * (angle + 135))

	def callback(self, msg):
		smallest = 100
		index = 0
		for i in range(0, 135):
			left = msg.ranges[self.angle_to_range(i)]
#			print(left, smallest)
			if left < smallest:
				smallest = left
				index = i
#		print(index)
		self.left = smallest

#		self.left = msg.ranges[self.angle_to_range(90)]
		self.front = msg.ranges[self.angle_to_range(0)]
		self.right = msg.ranges[self.angle_to_range(-90)]

	#	print(left)
	#	print(front)
	#	print(right)

if __name__ == '__main__':
	for i in range(-135,136):
		print(str(i) + " --> " + str(wall_hugger().angle_to_range(i)))

	try:
		wall_hugger()
	except rospy.ROSInterruptException: pass
