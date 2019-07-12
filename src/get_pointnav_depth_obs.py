#!/usr/bin/env python
# note need to run viewer with python2!!!

import rospy
from rospy_tutorials.msg import Floats
from rospy.numpy_msg import numpy_msg
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from sensor_msgs.msg import PointCloud2
import sensor_msgs.point_cloud2 as pc2

import tf
import math

import cv2
import numpy as np
import time
import pickle

# class NN_sensor():
#     def __init__(self):
#         self.depth=None
#         self.goal=None

pub_depth_and_pointgoal = rospy.Publisher(
    "depth_and_pointgoal", numpy_msg(Floats), queue_size=10
)
linear = None
angular = None


def listener():
    global linear
    global angular

    def callback(cloud):
        print('call back entered')

        bridge = CvBridge()
        cv_image = bridge.imgmsg_to_cv2(cloud, desired_encoding="passthrough")
        img_copy = np.copy(np.float32(cv_image))

        print("inside call back linear is " + str(linear))
        print("inside call back angular is " + str(angular))
        if img_copy.shape == (256, 256):

            inds = np.where(np.isnan(img_copy))

            MAX_DEPTH = 10
            img_copy[inds] = MAX_DEPTH
            img_copy = (img_copy-0.2)/10
            pickle.dump( img_copy, open( "foo.p", "wb" ) )
            depth_np = np.float32(img_copy.ravel())
            pointgoal_np = np.float32([linear, angular])
            depth_pointgoal_np = np.concatenate((depth_np, pointgoal_np))
            pub_depth_and_pointgoal.publish(np.float32(depth_pointgoal_np))

            # cv2.imshow("Depth", img_copy)
            # cv2.waitKey(100)
            # time.sleep(0.2)

    rospy.init_node("depth_distance")
    # sub = rospy.Subscriber("/camera/depth/points", PointCloud2, callback)

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

    print("trans is initialized")
    (trans, rot) = tf_listner.lookupTransform("/base_footprint", "/goal", rospy.Time(0))

    angular = math.atan2(trans[1], trans[0])
    linear = 0.5 * math.sqrt(trans[0] ** 2 + trans[1] ** 2)
    print(linear)

    sub = rospy.Subscriber("/camera/depth/image_raw", Image, callback)

    while not rospy.is_shutdown():
        try:
            (trans, rot) = tf_listner.lookupTransform(
                "/base_footprint", "/goal", rospy.Time(0)
            )
        except (
            tf.LookupException,
            tf.ConnectivityException,
            tf.ExtrapolationException,
        ):
            continue

        angular = math.atan2(trans[1], trans[0])
        linear = 0.5 * math.sqrt(trans[0] ** 2 + trans[1] ** 2)
        # print("linear is " + str(linear))
        # print("angular is " + str(angular))

        rate.sleep()


if __name__ == "__main__":
    listener()
