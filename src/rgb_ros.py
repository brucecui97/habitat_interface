#!/usr/bin/env python
# note need to run viewer with python2!!!

import rospy
from rospy_tutorials.msg import Floats
from rospy.numpy_msg import numpy_msg
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image

import cv2
import numpy as np


pub = rospy.Publisher("ros_img_rgb", Image, queue_size=10)


def callback(data):
    img = (np.reshape(data.data, (720, 720, 3))).astype(np.uint8)
    image_message = CvBridge().cv2_to_imgmsg(img, encoding="rgb8")
    pub.publish(image_message)


def listener():
    rospy.init_node("rgb2ros_rgb")
    rospy.Subscriber("rgb", numpy_msg(Floats), callback)
    rospy.spin()


if __name__ == "__main__":
    listener()
