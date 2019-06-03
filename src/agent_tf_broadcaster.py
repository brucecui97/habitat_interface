#!/usr/bin/env python  
PKG = "numpy_tutorial"
import roslib

roslib.load_manifest(PKG)

import rospy
from rospy.numpy_msg import numpy_msg
from rospy_tutorials.msg import Floats
import tf


def handle_agent_pose(msg,agentname):
    pose_array=msg.data
    habitat_quaternion_orient = pose_array[3:]
    (roll, pitch,yaw) = tf.transformations.euler_from_quaternion(habitat_quaternion_orient)
    #ros_quaternion_orient = tf.transformations.quaternion_from_euler(yaw,roll,pitch) 
   
    #why is quaternion backwards??????
    ros_quaternion_orient = (-habitat_quaternion_orient[0],-habitat_quaternion_orient[2],-habitat_quaternion_orient[1],-habitat_quaternion_orient[3])
    #ros_quaternion_orient = (habitat_quaternion_orient[0],habitat_quaternion_orient[1],-habitat_quaternion_orient[2],habitat_quaternion_orient[3])
    
    print(yaw)
    br1 = tf.TransformBroadcaster()
    br1.sendTransform((-pose_array[2], -pose_array[0], 0),
                     ros_quaternion_orient,
                     rospy.Time.now(),
                     agentname,
                     "map")

    br2 = tf.TransformBroadcaster()
    br2.sendTransform((-pose_array[2], -pose_array[0], 0),
                     ros_quaternion_orient,
                     rospy.Time.now(),
                     "camera_depth_frame",
                     "map")
    print('handle_agent_pose_called')

if __name__ == '__main__':
    rospy.init_node('agent_tf_broadcaster')
    agentname = "bruce_agent"
    rospy.Subscriber('agent_pose',
                     numpy_msg(Floats),
                     handle_agent_pose,
                     agentname)
    rospy.spin()

  #    br1.sendTransform((-pose_array[2], -pose_array[0], 0),
   #                  (pose_array[3],-pose_array[6],-pose_array[4],pose_array[5]),
    #                 rospy.Time.now(),
     #                agentname,
      #               "world")