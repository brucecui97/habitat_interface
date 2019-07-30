#!/usr/bin/env python
import pytest
import rospy
from time import sleep
from sensor_msgs.msg import Image

def test_depth_ros():

    is_ros_depth_publishing=False

    def callback(data):
        global is_ros_depth_publishing
        is_ros_depth_publishing = True
        

    rospy.init_node('test_ros_rgb')
    rospy.Subscriber('ros_img_depth',Image,callback)
    counter = 0
    while not rospy.is_shutdown() and counter <5 and (not is_ros_depth_publishing):
        sleep(1)
        counter += 1

    assert (is_ros_depth_publishing == True), 'habitat depth is not being converted and published as ros img depth'

