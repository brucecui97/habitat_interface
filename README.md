# Habitat ROS Interface


## Objective

Connect Facebook's AI Habitat simulator environment with ROS so that traditional ROS packages such as SLAM and navigation can be used.

## Demos

<p align="left">
  <img src="res/habitat_interface.gif"  height="400">
</p>

Navigating Habitat environment with ROS navigation package: https://youtu.be/VYfZ4wghpRA

Navigating Gazebo (ROS' simulator) environment with Habitat trained agent: https://youtu.be/EaU_a6MIeIE

Navigating Habitat environment with Habitat trained agent with ROS in the loop: https://youtu.be/eYywGkWd_0E

Slide deck for demo purposes: https://1drv.ms/p/s!AhI7FLXI6kP7hfA3lsetrnm2y0Uq9g


## High Level Design

![implementation](images/implementation.png)


## Dependencies (Tested on Ubuntu 16.04 using ROS kinetic)

ROS Kinetic (http://wiki.ros.org/kinetic)

    *depthimage_to_laserscan
    *laser_scan_matcher
    *hector_slam [needed during mapping and navigation]

Anaconda (https://www.anaconda.com/distribution/) 


## Installation Procedures
1. Clone this repository into your catkin_ws/src folder
2. Run `cd ~/catkin_ws && catkin_make`(replace catkin_ws with your own workspace name if applicable)
3. Install ROS' depthimage_to_laserscan, laser_scan_matcher, and hector_slam packages by running `sudo apt-get install ros-kinetic-depthimage-to-laserscan`,  `sudo apt-get install ros-kinetic-laser-scan-matcher`, and `sudo apt-get install ros-kinetic-hector-slam`. If you encounter errors relating to "cannot find package", this link helped me solve the problem https://answers.ros.org/question/325039/apt-update-fails-cannot-install-pkgs-key-not-working/
4. [Anaconda environment with python>=3.6 is needed for this step] Install habitat-api with instructions here  https://github.com/brucecui97/habitat-api, but DO NOT install habitat-sim using the links given in this repo. Instead, install habitat-sim by following this link https://github.com/brucecui97/habitat-sim/tree/lci2019s. Specifically, the "Developer installation and getting started" section. (Note you do not need to install these in a catkin workspace)
5. Resolve errors you encounter when installing habitat-api and habitat-sim by seeing their issues page in Facebook's repos first. (https://github.com/facebookresearch/habitat-api and https://github.com/facebookresearch/habitat-sim)

The following steps ensure you can run Anaconda along side ROS (we need Anaconda because Habitat requires python>=3.6 while ROS requires python2)

6. In the Anaconda environment you used to install habitat-api and habitat-sim, run `pip install rospkg` so the file habitat-api/habitat_ros/hab_ros_plant.py can be ran from your Python3.6 Anaconda environment
7. If your setup.bash files related to ROS is automatically being sourced by ~/.bashrc, remove that so you won't run into errors because of ROS adding "/opt/ros/kinetic/lib/python2.7/dist-packages" to your python path. (e.g. If you don't you would get the following error when importing cv2 in a Python3.6 Anaconda environment: "/opt/ros/kinetic/lib/python2.7/dist-packages/cv2.so: undefined symbol: PyCObject_Type". (more details about this issue can be found here: https://stackoverflow.com/questions/43019951/after-install-ros-kinetic-cannot-import-opencv)
8.  [Recommended] Add an alias to the sourcing commands of your ROS setup.bash files

The following picture shows how I modified my ~/.bashrc file to complete steps 7 and 8

![sros_alias](images/sros_alias.png)

### Installation Procedure Justifications
1. NA
2. NA
3. Normally ROS does not come with these packages
4. You need habitat api and habitat sim installed to run simulator back-end. The installation links point to my repos because this allows you to use the ROS interface with settings I preconfigured. Please note that the main difference between my forked habitat-api repo and the Facebook's habitat-api repo is that I added the habitat_ros folder and some task config .yaml files. Similarly, I made no modifications to Facebook's habitat-sim repo, but only added a tag indicating the habitat-sim version I tested on
5. NA
6. This step installs a new rospkg in your anaconda environment since the one you installed with your ROS distribution is done using apt-get which installs to your system's default python directory (not the Anaconda directory you installed Habitat in). After this step, you can use rospkg functionalities in your anaconda environment with python>=3.6. In short, this step ensures ROS works in an Anaconda environment with python>=3.6
7. This step allows you to not add ROS paths by default and only add the paths when you need ROS. 
8. This step allows you to add ROS required paths more easily

## Running Habitat with ROS

1. Activate your anaconda python>=3.6 and cd into habitat-api's root directory
2. Source your ROS related setup.bash files
3. cd into the habitat-api directory
4. Run `python habitat_ros/hab_ros_interface.py` to run the node that publishes on habitat sensor reading topics and subscribes to the /cmd_vel topic

5.  Deactivate Anaconda as you won't need python>=3.6 anymore to interact with the Habitat back-end (This step is hacky. I usually just go inside my ~/.bashrc and comment/uncomment the lines related to Anaconda manually depending on whether or not I need Anaconda)

    ![conda](images/conda.png) 

6. close and re-open your terminal
7. Source your ROS related setup.bash files again and run `roslaunch habitat_interface default.launch` to convert all habitat sensor messages into ROS messages  (e.g.  numpy image to ROS image).  This launch file also launches a joystick controller to control the habitat agent along with visualization tools such as image view

Launch files for running hector_mapping (hector_map.launch) and navigation (move_base.launch) are also included. First run default.launch, then run either hector_map.launch or move_base.launch. Note that to run navigation, you need to change the value of the "map_path" variable in move_base.launch to point to the map you want to use. In addition, you can use the get_ros_map.py script in habitat-api/habitat_ros to generate a ROS/Rviz compatible map that you can compare/overlay with your SLAM generated map to evaluate the SLAM generated map's accuracy (you'll need to modify the origin of your map.yaml file to have the two maps line up in Rviz).



   
### Publish/subscribed topics by hab_ros_interface.py

Published:

 * /habitat/depth [rospy_tutorials/Floats]
 * /rosout [rosgraph_msgs/Log]
 * /habitat/rgb [rospy_tutorials/Floats] 
 * /depth_and_pointgoal [rospy_tutorials/Floats] 

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

You can modify the _update_position and _update_attitude methods in the sim_env class in hab_ros_interface.py to change the robot's behaviour at each time step. (e.g. you can specify that the robot has a maximum acceleration of 0.1m/s^2)

#### Changing Sensor Publishing Frequency
Change the _sensor_rate class variable in hab_ros_interface.py

#### Changing number of sensors
See habitat-api/examples/register_new_sensors_and_measures.py for details. 

As an example, I added an additional sensor called BC_SENSOR (this is just another RGB sensor) and you can access the readings of this sensor if you add this sensor to your config file (see screenshot below as an example). You can obtain its values by calling `self.observations['bc_sensor']` in hab_ros_interface.py

![bc_sensor](images/bc_sensor.png)


## Future work 

### Installation and Running Related
1. Place habitat-api in a catkin work space (i.e. make Habitat a ROS package). The advantage of wrapping Habitat in a catkin_ws is that we can use launch files to remap topics and do unit and integration tests. The main difficulty of this implementation  is that most of habitat's files specify relative paths, while ROS commands such as rosrun and roslaunch sets "the working directory of all nodes to $ROS_HOME, which in most cases will be $HOME/.ros" (source: https://answers.ros.org/question/235337/unable-to-read-a-file-while-using-relative-path/)
 
    Therefore, to wrap habitat in a catkin_package, we either need to change all paths in habitat-api (possibly also habitat-sim) to be absolute paths, or need to somehow use ROS' `rospack find` feature (`$find some_package` feature in ROS launch files) to change all relative paths to absolute paths at run time.

    Below is an image showing a sample habitat episode specification file. You can see the path to the scene is relative to habitat-api's root directory.

    ![episode_spec_data](images/episode_spec_data.png)

2. Simplify the procedures to run Habitat with ROS. For example, eliminate the need to manually comment out Anaconda related lines in ~/.bashrc to run system's default ROS. Currently I'm searching/developing a robust method to run ROS in a python2.7 Anaconda environment.

### Development Related

1. Add unit tests and ROS node tests
2. Add feature to modify geometry of habitat agent. For example, change the agent radius and height and/or change the agent shape to be a rectangle. My current thoughts is to modify the NavMeshSettings. (The thing that generates the navmeshes is  https://github.com/facebookresearch/habitat-sim/blob/master/src/utils/datatool/datatool.cpp  and the NavMeshSettings are the thing that specify the agent's radius: https://github.com/facebookresearch/habitat-sim/blob/master/src/esp/nav/PathFinder.h. Therefore, I think changing the `agentRadius` value should change the dimension of the agent
3. Add feature to change angular position of rgb/depth sensors. This file https://github.com/facebookresearch/habitat-sim/blob/master/src/esp/sensor/Sensor.h#L38 should be helpful and doing sensor_spec.orientation = [0, np.pi, 0]should do it [Erik from the Habitat team kindly told me this]
4. Create a method to overlay the ground truth map generated with get_ros_map.py and a map generated through SLAM. This allows users to compare AMCL generated pose/odom with the ground truth pose/odom. Currently to overlay these two maps I am manually changing the `origin` value in the SLAM generated map's  .yaml file. In the future, this step could possibly be automated by some vision/optimization technique that shifts one map's origin. Additionally, by understanding how SLAM packages like hector_slam creates its map.pgm and map.yaml, we can do things like crop the map.pgm picture in a way such that only relevant pixels remain (grey pixels surrounding the map are cropped away). This allows us to potentially select the bottom left corner of both the SLAM generated and ground truth map to be the map origin and overlay the two maps. 
5. Create a method to extract the ground truth position of the habitat agent relative to the ground truth map. A work in progress version is available here https://github.com/brucecui97/habitat-api/blob/add_gt_pose/habitat_ros/hab_ros_interface.py#L138-L165. The idea is that we can extract the agent_map_coord from the top down map in pixels, then convert the pixel into meters. 
6. Add more complex motion model to the agent. E.g. specify that the agent can only accelerate at a maximum of `X` m/s^2. This can be done by modifying the _update_position and _update_attitude methods in the sim_env class in hab_ros_interface.py 
7. (Just for fun) Continue developing code that transfers a Habitat trained agent to the real world (pyrobot is also working on this). I created a proof of concept script ( habitat-api/habitat_baselines/eval_habitat_agent_in_ros.py)  in June 2019, but the code might be outdated

When adding new features, please note that in the habitat environment, the agent looks along the -z axis,and to the right of where the agent looks is the -x axis. Above the agent is the +y axis

## References and Citation
1. [Habitat: A Platform for Embodied AI Research](https://arxiv.org/abs/1904.01201). Manolis Savva, Abhishek Kadian, Oleksandr Maksymets, Yili Zhao, Erik Wijmans, Bhavana Jain, Julian Straub, Jia Liu, Vladlen Koltun, Jitendra Malik, Devi Parikh, Dhruv Batra. IEEE/CVF International Conference on Computer Vision (ICCV), 2019.
