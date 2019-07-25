# Habitat ROS Interface

## Motivation
Real world robots move in a continous environment. To this end, we aim to to build on top of the existing Habitat simulator to create a realistic agent transversing through the highly photorealistic 3D environments with ROS connectivity.

## Goals

1. Connect Habitat simulator environment with ROS so that traditional ROS packages for SLAM and navigation can be used​
2. Test discrete action space trained agents in a kinematic environment​
3. Test discrete action space trained agents in a traditional robotics simulation environment (Gazebo) with complex physcics 

## Design

See one drive diagram

## API

Not applicable

## Dependencies

ROS1 (this is likely to change as we evaluate the new ROS2 platform)
Anaconda
habitat-api
habitat-sim

## Testing

No tests written at current stage. Coming soon.v

### Functional Testing

Coming soon

### Performance Testing

Coming soon

### Scale Testing

Coming soon

## Installation

1. Clone this repository into your catkin_ws/src folder
2. run cd ~/catkin_ws && catkin_make
3. get laser scan matcher by running sudo apt-get install ros-kinetic-laser-scan-matcher
4. Clone habitat-api and follow installation instructions at https://github.com/brucecui97/habitat-api
5. If you have trouble installing habitat-api or sim, see habitat's issues page first. An error I encountered regularly in the past is the "ModuleNotFoundError: No module named 'habitat_sim._ext'" and my hacky way around it is to copy the _ext folder from your build directory (/habitat-sim/build/lib.linux-x86_64-3.6/habitat_sim) to (/habitat-sim/habitat_sim)
6. Copy the habitat_ros folder into habitat-api's root directory
7. Download gibson datasets in from habitat-api's repository if you want to use this data set
8. In your Anaconda environment (python version >=3.6), run pip install rospkg (hacky solution) one time so hab_ros_plant.py can be ran
9. If your setup.bash files related to ROS is automatically being sourced by ~/.bashrc, remove that and I recommend adding an alia to the sourcing commands of your setup.bash files
10. Ensure you can run both ROS and habitat_ros_interface correctly

## Running (section will probably be change into a colored diagram like gazebo_ros interface)

### habitat-api/habitat_ros/hab_ros_plant.py

This is a script/node that interfaces with the Habitat simulator backend

subscribed topics: /cmd_vel
published topics: 

        self._pub_rgb = rospy.Publisher("rgb", numpy_msg(Floats), queue_size=1)
        self._pub_depth = rospy.Publisher("depth", numpy_msg(Floats), queue_size=1)
        self._pub_depth_and_pointgoal = rospy.Publisher(
            "depth_and_pointgoal", numpy_msg(Floats), queue_size=1
        )

### Habitat_interface package 
    
this package provides an interface with the habitat back end to convert numpy sensor readnigs to ros images. launch files for joy control, mapping, navigation are all included. See them for examples on how to utilze this package.

For example, run roslaunch habitat_interface default.launch to begin publishing ROS depth readings, joy controlller, rgb readings joy readings, laser scans

And also launche nodes to visualize the rgb_camera with image_view.

### Changing scenes

To change scenes, change the config file fed into the environmnet initalizer in hab_ros_interface.py. See habitat-api for a list of scens available and how to write the config files

### Changing robot dynamics

You can modify the update_position and update_attitude methods to change the robot's behaviour at each time step. (e.g. you specifiy how the robot can only accelerate at 0.1m/s^2)
