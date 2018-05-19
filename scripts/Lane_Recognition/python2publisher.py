#!/usr/bin/env python2
import rospy
import sys
from std_msgs.msg import String
from geometry_msgs.msg import Pose2D

def talker():
	pub = rospy.Publisher('point_in', Pose2D, queue_size=10)
	rospy.init_node('Py3toROS', anonymous=True)
	rate = rospy.Rate(10)
	_ = sys.stdin.readline()
	while not rospy.is_shutdown():
		#for line in sys.stdin:
		input = sys.stdin.readline()
		if input != "":
			#hello_str = "hello world %s" % input
			#rospy.loginfo(hello_str)
			data = eval(input)
			pubmsg = Pose2D(data[0], data[1], 0)
			pub.publish(pubmsg)
			rate.sleep()


if __name__ == '__main__':
	try:
		talker()
	except rospy.ROSInterruptException:
		pass
