#!/usr/bin/env python
# note need to run viewer with python2!!!

import rospy
from rospy_tutorials.msg import Floats
from rospy.numpy_msg import numpy_msg
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image

import cv2
import numpy as np

rospy.init_node("npbc_sensor2ros_rgb",anonymous=False)

pub = rospy.Publisher("ros_img_bc_sensor", Image, queue_size=10)


def callback(data):
    img_raveled = data.data[0:-2]
    img_size = data.data[-2:].astype(int)

    img = (np.reshape(img_raveled, (img_size[0], img_size[1], 3))).astype(np.uint8)
    image_message = CvBridge().cv2_to_imgmsg(img, encoding="rgb8")
    pub.publish(image_message)


def listener():
    
    rospy.Subscriber("rgb", numpy_msg(Floats), callback)
    rospy.spin()


if __name__ == "__main__":
    listener()
