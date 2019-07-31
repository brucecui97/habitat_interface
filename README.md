# Habitat ROS Interface

## Objective

Connect Facebook's AI Habitat simulator environment with ROS so that traditional ROS packages such as SLAM and navigation can be used.

## High Level Design

![implementation](images/implementation.png)


## Dependencies (Tested on Ubuntu 16.04 using ROS kinetic)

(TODO confirm dependencies by following instructions here: https://stackoverflow.com/questions/42237072/list-dependencies-in-python)

ROS Kinetic

habitat-api

habitat-sim


## Installation Procedures

1. Clone this repository into your catkin_ws/src folder
2. Run `cd ~/catkin_ws && catkin_make`
3. Install ROS' laser scan matcher package by running `sudo apt-get install ros-kinetic-laser-scan-matcher`
4. [Anaconda environment with python>=3.6 is needed for this step] Install habitat-api and habitat-sim by following their installation instructions at https://github.com/facebookresearch/habitat-api. Download any of the datasets provided by Habitat that you would like to use  (TODO decide whether to link to my repo instead)
5. Resolve errors you encounter when installing habitat-api or sim by seeing their respective issues page first. An error I encountered regularly when installing habitat-sim is the "ModuleNotFoundError: No module named 'habitat_sim._ext'" and my hacky way around it is to copy the _ext folder from the build directory (/habitat-sim/build/lib.linux-x86_64-3.6/habitat_sim) to (/habitat-sim/habitat_sim) (TODO maybe ask Habitat people why after trying to install on new machine again first)
6.  Cut and paste the habitat_ros folder in this repo into habitat-api's root directory

The following steps ensure you can run Anaconda along side ROS (we need Anaconda because Habitat requires python>=3.6 while ROS requires python2)

7. In the Anaconda environment you used to install habitat-api and habitat-sim, run pip install rospkg so the file habitat-api/habitat_ros/hab_ros_plant.py can be ran from your Python3.6 Anaconda environment
8. If your setup.bash files related to ROS is automatically being sourced by ~/.bashrc, remove that so you won't run into errors because of ROS adding "/opt/ros/kinetic/lib/python2.7/dist-packages" to your python path. (e.g. If you don't you would get the following error when importing cv2 in a Python3.6 Anaconda environment: "/opt/ros/kinetic/lib/python2.7/dist-packages/cv2.so: undefined symbol: PyCObject_Type". (more details about this issue can be found here: https://stackoverflow.com/questions/43019951/after-install-ros-kinetic-cannot-import-opencv)
9.  [optional] Add an alias to the sourcing commands of your ROS setup.bash files

The following picture shows how I modified my ~/.bashrc file to complete steps 8 and 9

![sros_alias](images/sros_alias.png)

### Installation Procedure Justifications
1. NA
2. NA
3. Normally ROS does not come with laser scan matcher package, which is needed for visual odometry
4. You need habitat api and habitat sim installed to run simulator backend
5. NA
6. The habitat_ros folder contains the ROS plugin (python module) to interface with Habitat's backend. I recommend cutting and pasting this folder instead of copying and pasting because this folder shouldn't belong in a ROS package. In the future, the habitat_ros folder might be merged with habitat-api's repository so you won't have to do this step
7. This step installs a new rospkg in your anaconda environment since the one you installed with your ROS distribution is done using apt-get which installs to your system's default python directory, and not the Anaconda directory you installed Habitat in. After this step, you can use rospkg functionalities in your anaconda environment with python>=3.6. In short, this step ensures ROS works in an Anaconda environment with python>=3.6
8. This step allows you to not add ROS paths by default and only add the paths when you need ROS. 
9. This step allows you to add ROS required paths more easily

## Running Habitat with ROS

1. Activate your anaconda python>=3.6 and cd into habitat-api's root directory
2. Source your ROS related setup.bash files
3. Run `python habitat_ros/hab_ros_interface.py` to run the node that publishes on habitat sensor reading topics and subscribes to the /cmd_vel topics

4. Deactivatie Anaconda and or switch to a ROS compatible python 2.7 environment, as you won't need python>=3.6 anymore to interact with the Habitat backend
 
5. Run `roslaunch habitat_interface default.launch` to convert all habitat sensor messages into ROS mssageses (e.g.  numpy image to ROS image).  This launch file also launches a joystick controller to control the habitat agent along with visualization tools such as rviz, rqt_graph, and image view

In addition, launch files for running hector_mapping (hector_map.launch) and navigation (move_base.launch) are also included. First run default.launch, then run either hector_map.launch or move_base.launch.

<!-- 
This launch file also ensure all of the custom habitat sensor topics are being converted to ROS topics (e.g. numpy image converted to ROS image). Most notably, there is a node in this launch file to convert a depth image into laser scan. -->
   
### Publish/subscribed topics by hab_ros_interface.py

Published:

 * /habitat/depth [rospy_tutorials/Floats]
 * /rosout [rosgraph_msgs/Log]
 * /habitat/rgb [rospy_tutorials/Floats] 
 by default.launch)
 * /depth_and_pointgoal [rospy_tutorials/Floats] (

Subscribed
* /cmd_vel [geometry_msgs/Twist]

### Modifying Habitat Simulator Settings

You can change simulator settings by modifying the hab_ros_interface.py file.

#### Changing Scenes

To change scenes, change the config file fed into the environment initializer in hab_ros_interface.py. 

```python
my_env = sim_env(env_config_file="path/to/your/custom/config/file.yaml")
```
Specifically, inside your config file, modify the DATASET tag. See screenshot below for an example

![data_path](images/data_path.png)

#### Changing Robot Dynamics

You can modify the _update_position and _update_attitude behaviours/methods in the sim_env class in hab_ros_interface.py to change the robot's behaviour at each time step. (e.g. you can specifiy that the robot has a maximum acceleration of 0.1m/s^2)

#### Changing Sensor Publishing Freuqency
Change the _sensor_rate class variable in hab_ros_interface.py

## Testing
TODO (Haibtat uses pytest, and currently I'm learning how to use pytest with ROS)

## Future work 

1. Place Habitat in a catkin work space (i.e. make Habitat a ROS package). The advantage of wrapping Habitat in a catkin_ws is that we can use launch files to remap topics and do unit and integration tests. The main difficulty of this implmentation is that most of habitat's files specify relative paths, while ROS commands such as rosrun and roslaunch sets "the working directory of all nodes to $ROS_HOME, which in most cases will be $HOME/.ros" (source: https://answers.ros.org/question/235337/unable-to-read-a-file-while-using-relative-path/)
 
    Therefore, to wrap habitat in a catkin_package, we either need to change all paths in habitat-api (possibly also habitat-sim) to be absolute paths, or need to somehow use ROS' `rospack find` feature (`$find some_package` feature in ROS launch files) to change all relative paths to absolute paths at run time.

    Below is an image showing a sample habitat episode specification file. You can see the path to the scene is relative to habitat-api's root directory.

    ![episode_spec_data](images/episode_spec_data.png)

2. Add a simple script to convert habitat generated top down maps to ROS/Rviz compatible maps so that ground truth map can be displayed when doing ROS navigation
3. Improve multithreading implementation of hab_ros_interface.py to optimize for performance
4. Add unit tests and ROS node tests

