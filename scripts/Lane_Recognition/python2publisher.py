#!/usr/bin/env python2
import rospy
import sys
from std_msgs.msg import String
from geometry_msgs.msg import Vector3

def talker():
	pub = rospy.Publisher('chatter', Vector3, queue_size=10)
	rospy.init_node('talker', anonymous=True)
	rate = rospy.Rate(10)
	while not rospy.is_shutdown():
		#for line in sys.stdin:
		input = sys.stdin.readline()
		if input != "":
			#hello_str = "hello world %s" % input
			#rospy.loginfo(hello_str)
			data = eval(input)
			pubmsg = Vector3(data[0], data[1], 0)
			pub.publish(pubmsg)
			rate.sleep()


if __name__ == '__main__':
	try:
		talker()
	except rospy.ROSInterruptException:
		pass
