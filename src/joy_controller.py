#!/usr/bin/env python
PKG = 'numpy_tutorial'
import roslib; roslib.load_manifest(PKG)

import rospy
from rospy_tutorials.msg import Floats
from rospy.numpy_msg import numpy_msg
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist
import sys

sys.path=sys.path[3:]
import cv2
import numpy as np


pub1 = rospy.Publisher('cmd_vel', Twist,queue_size=10)

# Author: Andrew Dai
def callback(data):
    #negative sign in vel_z because agent eyes look at negative z axis
    vel_max=10 #m/s
    vel_z=4*data.axes[1]*vel_max*0.001
    #something to do with the joy contrller is wrong as pushing right seems to be negative
    vel_x=-4*data.axes[0]*vel_max*0.001

    #again negative because of joy controller
    yaw=data.axes[3]
    pitch=data.axes[4]
    
    vel_msg = Twist()
    vel_msg.linear.x=vel_z
    vel_msg.linear.y=vel_x
    vel_msg.linear.z=0
    vel_msg.angular.x = 0
    vel_msg.angular.y = pitch
    vel_msg.angular.z = yaw

    pub1.publish(vel_msg)

# Intializes everything
def start():
    rospy.init_node('Joy2Turtle')
    rospy.Subscriber("joy", Joy, callback)
    # starts the node
    rospy.spin()

if __name__ == '__main__':
    start()
