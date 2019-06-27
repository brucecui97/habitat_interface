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

def listener():
    def callback(cloud):
        print("call back entered")
        bridge=CvBridge()
        cv_image = bridge.imgmsg_to_cv2(cloud, desired_encoding="passthrough")
        cv2.imshow("rgb",cv_image)
        cv2.waitKey(100)
        time.sleep(3)
        print (cv_image.shape)

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
    #sub = rospy.Subscriber("/camera/depth/points", PointCloud2, callback)
    sub = rospy.Subscriber("/camera/depth/image_raw", Image, callback)
    rospy.spin()


if __name__ == "__main__":
    listener()
