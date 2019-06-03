#!/usr/bin/env python
PKG = 'numpy_tutorial'
import roslib; roslib.load_manifest(PKG)

import rospy
from rospy_tutorials.msg import Floats
from rospy.numpy_msg import numpy_msg
from sensor_msgs.msg import Joy
import sys
sys.path=sys.path[3:]
import cv2
import numpy as np


pub1 = rospy.Publisher('linear_vel_command', numpy_msg(Floats),queue_size=10)
pub2 = rospy.Publisher('angular_vel_command', numpy_msg(Floats),queue_size=10)
# Author: Andrew Dai
def callback(data):
    vel_max=10 #m/s
    vel_z=4*data.axes[1]*vel_max*0.001
    vel_x=4*data.axes[0]*vel_max*0.001
    #negative sign in vel_z because agent eyes look at negative z axis
    linear_vel_to_publish=np.float32([-vel_z,-vel_x])

    yaw=data.axes[3]
    pitch=data.axes[4]
    angular_vel_to_publish=np.float32([pitch,yaw])

    vel_to_publish=np.float32([linear_vel_to_publish,angular_vel_to_publish]).ravel()
    print("joy_controller published" + str(vel_to_publish))
    pub1.publish(vel_to_publish)


    pub2.publish(angular_vel_to_publish)

# Intializes everything
def start():
    rospy.Subscriber("joy", Joy, callback)
    # starts the node
    rospy.init_node('Joy2Turtle')
    rospy.spin()

if __name__ == '__main__':
    start()
