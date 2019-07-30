#!/usr/bin/env python
import unittest
import rospy
import pytest
from sensor_msgs.msg import Image
from time import sleep
import rostest

class TestRgbROS(unittest.TestCase):
    is_ros_rgb_publishing = False
    def callback(self,data):
        self.is_ros_rgb_publishing = True
        pass

    def test_rgb_ros(self):
        rospy.init_node('test_ros_rgb')
        rospy.Subscriber('ros_img_rgb',Image,self.callback)
        counter = 0
        while not rospy.is_shutdown() and counter <5 and (not self.is_ros_rgb_publishing):
            sleep(1)
            counter += 1

        self.assertTrue (self.is_ros_rgb_publishing == True), 'ros rgb is not being converted and published as ros img rgb'
    
if __name__ == "__main__":
    rostest.rosrun('habitat_interface','test_rgb_ros',TestRgbROS)