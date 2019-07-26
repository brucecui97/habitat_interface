#!/usr/bin/env python
# note need to run viewer with python2!!!

import rospy
from rospy_tutorials.msg import Floats
from rospy.numpy_msg import numpy_msg
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image

import tf
import math

import cv2
import numpy as np


pub_depth_and_pointgoal = rospy.Publisher(
    "depth_and_pointgoal", numpy_msg(Floats), queue_size=10
)


DEPTH_IMG_WIDTH = 720
DEPTH_IMG_HEIGHT = 720
MAX_DEPTH = 10
FAKE_DISTANCE_AMOUNT = 0.2


def listener():
    def callback(img):
        try:
            (trans, rot) = tf_listner.lookupTransform(
                "/base_footprint", "/goal", rospy.Time(0)
            )
        except:
            pass

        angular = math.atan2(trans[1], trans[0])
        linear = 0.5 * math.sqrt(trans[0] ** 2 + trans[1] ** 2)
        print("call back entered")

        cv_image = CvBridge().imgmsg_to_cv2(img, desired_encoding="passthrough")
        img_copy = np.copy(np.float32(cv_image))

        print("inside call back linear is " + str(linear))
        print("inside call back angular is " + str(angular))
        if img_copy.shape == (DEPTH_IMG_HEIGHT, DEPTH_IMG_WIDTH):
            inds = np.where(np.isnan(img_copy))
            img_copy[inds] = MAX_DEPTH

            # /10 from scaling factor of Habitat implmentation
            img_copy = (img_copy - FAKE_DISTANCE_AMOUNT) / 10

            depth_np = np.float32(img_copy.ravel())
            pointgoal_np = np.float32([linear, angular])
            depth_pointgoal_np = np.concatenate((depth_np, pointgoal_np))
            pub_depth_and_pointgoal.publish(np.float32(depth_pointgoal_np))

    rospy.init_node("depth_distance")
    linear = None
    angular = None
    rate = rospy.Rate(10.0)
    tf_listner = tf.TransformListener()

    trans = None
    while trans is None:
        try:
            (trans, rot) = tf_listner.lookupTransform(
                "/base_footprint", "/goal", rospy.Time(0)
            )
        except:
            pass

    angular = math.atan2(trans[1], trans[0])
    linear = 0.5 * math.sqrt(trans[0] ** 2 + trans[1] ** 2)

    rospy.Subscriber("/camera/depth/image_raw", Image, callback)

    rospy.spin()


if __name__ == "__main__":
    listener()
