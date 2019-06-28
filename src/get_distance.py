#!/usr/bin/env python
# note need to run viewer with python2!!!

import rospy
from rospy_tutorials.msg import Floats
from rospy.numpy_msg import numpy_msg
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from sensor_msgs.msg import PointCloud2
import sensor_msgs.point_cloud2 as pc2

import cv2
import numpy as np
import time
import pickle

pub_depth = rospy.Publisher("depth", numpy_msg(Floats), queue_size=10)
def listener():
    def callback(cloud):
        bridge = CvBridge()
        cv_image = bridge.imgmsg_to_cv2(cloud, desired_encoding="passthrough")
        img_copy = np.copy(np.float32(cv_image))
        if img_copy.shape == (256, 256):

            inds = np.where(np.isnan(img_copy))

            MAX_DEPTH = 10
            img_copy[inds] = MAX_DEPTH
            pub_depth.publish(img_copy.ravel())
            
            # pickle.dump(foo, open("foonan.p", "wb"))
            # pickle.dump( foo, open( "nofoonan.p", "wb" ) )
            # print(np.amax(foo))

            # print(type(foo))
            # print('foo was saved')
            # sub.unregister()
            # print('sub was unregistered')

        # gen = pc2.read_points(cloud, skip_nans=True, field_names=("x", "y", "z"))
        # print(sum(1 for x in gen))

        # print(type(gen))
        # for val in gen:
        #     #print(type(val))
        #     print(val.shape)

        # for p in pc2.read_points(cloud, field_names = ("x", "y", "z"), skip_nans=True):
        #     print " x : %f  y: %f  z: %f" %(p[0],p[1],p[2])

        # cloud_points = list(
        #     pc2.read_points(cloud, skip_nans=False, field_names=("x", "y", "z"))
        # )
        # pickle.dump( cloud_points, open( "bc.p", "wb" ) )
        # print('saved')
        # sub.unregister()

    print("listener started")
    rospy.init_node("depth_distance")
    # sub = rospy.Subscriber("/camera/depth/points", PointCloud2, callback)
    sub = rospy.Subscriber("/camera/depth/image_raw", Image, callback)
    rospy.spin()


if __name__ == "__main__":
    listener()
