#!/usr/bin/env python
import unittest
import rospy
import pytest
from rospy.numpy_msg import numpy_msg
from rospy_tutorials.msg import Floats
from time import sleep
import rostest

class TestRgbHabitat(unittest.TestCase):
    is_hab_rgb_publishing = False
    def callback(self,data):
        self.is_hab_rgb_publishing = True
        pass

    def test_rgb_hab(self):
        rospy.init_node('test_habitat_rgb')
        rospy.Subscriber('habitat/rgb',numpy_msg(Floats),self.callback)
        counter = 0
        while not rospy.is_shutdown() and counter <5 and (not self.is_hab_rgb_publishing):
            sleep(1)
            counter += 1

        self.assertTrue (self.is_hab_rgb_publishing == True), 'habitat rgb is not being converted and published as ros img rgb'
    
if __name__ == "__main__":
    rostest.rosrun('habitat_interface','test_rgb_hab',TestRgbHabitat)