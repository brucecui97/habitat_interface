#!/usr/bin/env python
PKG = 'numpy_tutorial'
import roslib; roslib.load_manifest(PKG)

import rospy
from rospy_tutorials.msg import Floats
from rospy.numpy_msg import numpy_msg
from sensor_msgs.msg import LaserScan


def callback(data):
    print(rospy.get_name(), "I heard %s" % str(data.intensities))
    print("call back called")
    

def listener():
    rospy.init_node('scan_listner_node')
    rospy.Subscriber("scan",LaserScan, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()