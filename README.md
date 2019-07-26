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

ROS
Anaconda
habitat-api
habitat-sim

## Testing

No tests written at current stage. Coming soon.

### Functional Testing

Coming soon

### Performance Testing

Coming soon

### Scale Testing

Coming soon

## Installation Procedures

1. Clone this repository into your catkin_ws/src folder
2. run cd ~/catkin_ws && catkin_make
3. get ROS'laser scan matcher package by running sudo apt-get install ros-kinetic-laser-scan-matcher
4. Clone habitat-api and habitat-sim and follow installation instructions at https://github.com/brucecui97/habitat-api. Download any of the datasets provided by Habitat that you would like to use (follow habitat's instructions on how to do that)
5. If you have trouble installing habitat-api or sim, see habitat's issues page first. An error I encountered regularly in the past is the "ModuleNotFoundError: No module named 'habitat_sim._ext'" and my hacky way around it is to copy the _ext folder from your build directory (/habitat-sim/build/lib.linux-x86_64-3.6/habitat_sim) to (/habitat-sim/habitat_sim)
6. Cut and paste the habitat_ros folder into habitat-api's root directory
7. In your Anaconda environment (python version >=3.6), run pip install rospkg (hacky solution) one time so hab_ros_plant.py can be ran
8. [Optional but recommended] If your setup.bash files related to ROS is automatically being sourced by ~/.bashrc, remove that and I recommend adding an alias to the sourcing commands of your setup.bash files
9.  Ensure you can run both ROS and habitat_ros_interface correctly

### Insllation Procedure Justifications
1. self explanatory
2. self explanatory
3. Normally ROS does not come with laser scan matcher package, which is needed for visual odometry (TODO confirm this)
4. You need habitat api and habitat sim as a backend to run it as a simulator
5. Generally you shouldn't run into a problem at this step, as the habitat installation should be well tested
6. The habitat_ros folder contains the plugin (python module) to interface with the Habitat backend, and this folder is not needed in your ROS package so I recommend cutting and pasting instead of copying and pasting
7. This step installs a new rospkg in your anaconda environment (the one you installed with your ROS distribution is done using apt-get which installs to the directory related to your python2.7 generally), so you can use rospkg functionalities in your anaconda environment with python>=3.6. In short, this step makes sure ROS plays nicely with Anaconda
8. This step allows you to add ROS required paths whenever you need ROS and get rid of them when you don't, so for instance you can run any habitat modules without issue just by not calling the alias that sources the ROS paths
9. self explanatory

## Running (section will probably be change into a colored diagram like gazebo_ros interface)
1. activate your anacnda python>=3.6 and cd into habitat-api's root directory
2. Run python habitat_ros/hab_ros_interface.py
3. Run roslaunch habitat_interface default.launch (here I recommend deactivating anaconda and or switching to a python 2.7 environment, as you won't have to interact with the habitat environment again during simulation). This will ensure all of the sensors are being published on the correct topics
4. Refer to the published subscribed topics below for details 

### habitat-api/habitat_ros/hab_ros_plant.py

This is a script/node that interfaces with the Habitat simulator backend

subscribed topics: /cmd_vel
published topics: 

        self._pub_rgb = rospy.Publisher("rgb", numpy_msg(Floats), queue_size=1)
        self._pub_depth = rospy.Publisher("depth", numpy_msg(Floats), queue_size=1)
        self._pub_depth_and_pointgoal = rospy.Publisher(
            "depth_and_pointgoal", numpy_msg(Floats), queue_size=1
        )

### Habitat_interface package explained
    
this package provides an interface with the habitat back end to convert numpy sensor readnigs to ros images. launch files for joy control, mapping, navigation are all included. See them for examples on how to utilze this package.

For example, run roslaunch habitat_interface default.launch to begin publishing ROS depth readings, joy controlller, rgb readings joy readings, laser scans

And also launche nodes to visualize the rgb_camera with image_view.

### Modifying Simulator Configurations

All changes to the simulation side can be done through the 1 single habitat plugin you previously placed in the habitat-api repository. 

#### Changing scenes

To change scenes, change the config file fed into the environmnet initalizer in hab_ros_interface.py. See habitat-api for a list of scens available and how to write the config files

#### Changing robot dynamics

You can modify the update_position and update_attitude methods to change the robot's behaviour at each time step. (e.g. you specifiy how the robot can only accelerate at 0.1m/s^2)
#### Changing sensor publishing freuqency
change the sensor fereqeuncy in the sim_env class


### Future work
attempting to wrap habitat in a catkin work space; however, the main difficulty is that most of habitat's paths used in their scripts use relative paths, but rosrun/roslaunch sets ites default path to ~/.ros (confirm this), so to wrap habitat in a catkin_package, I either need to change all paths in the habitat environment to be absolute paths, or need to somehow use ROS' rospack find or ($find some_package in launch file) feature to change paths

improving the mulithreading implementation of the plug in to optmize for performance

add a simple script to convert habitat's top down map to ROS compatitible map with Rviz so ground truth map exists when doing ROS navigation

add sensors to the robot so can have multiple views at one time when opearting the agent




