#!/usr/bin/env python  
PKG = "numpy_tutorial"
import roslib

roslib.load_manifest(PKG)

import rospy
from rospy.numpy_msg import numpy_msg
from rospy_tutorials.msg import Floats
import tf
import numpy as np
import quaternion


def handle_agent_pose(msg,agentname):
    pose_array=msg.data
    habitat_quaternion_orient = pose_array[3:]
    print(habitat_quaternion_orient)
    (roll, pitch,yaw) = tf.transformations.euler_from_quaternion(habitat_quaternion_orient)
    #ros_quaternion_orient = tf.transformations.quaternion_from_euler(yaw,roll,pitch) 
   
    #why is quaternion backwards??????
    ros_quaternion_orient = np.quaternion(habitat_quaternion_orient[0],-habitat_quaternion_orient[3],-habitat_quaternion_orient[1],habitat_quaternion_orient[2])
    #ros_quaternion_orient = np.quaternion(habitat_quaternion_orient[0],-habitat_quaternion_orient[3],habitat_quaternion_orient[1],habitat_quaternion_orient[2])
    #ros_quaternion_orient = np.quaternion(0,0,0,1) * ros_quaternion_orient
    ros_quaternion_orient = (ros_quaternion_orient.x,ros_quaternion_orient.y,ros_quaternion_orient.z,ros_quaternion_orient.w)

    #print(tf.transformations.quaternion_from_euler(0,0,1))
    #ros_quaternion_orient = (habitat_quaternion_orient[0],habitat_quaternion_orient[3],-habitat_quaternion_orient[2],habitat_quaternion_orient[1])
    
    br1 = tf.TransformBroadcaster()
    br1.sendTransform((-pose_array[2], -pose_array[0], pose_array[1]),
                     ros_quaternion_orient,
                     rospy.Time.now(),
                     agentname,
                     "nav")

    br2 = tf.TransformBroadcaster()
    br2.sendTransform((-pose_array[2], -pose_array[0], pose_array[1]),
                     ros_quaternion_orient,
                     rospy.Time.now(),
                     "camera_depth_frame",
                     "nav")
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