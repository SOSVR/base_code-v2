SOSvr Base Code 2.0
---  

*Please cite this [paper](http://www.robocup2016.org/media/symposium/Team-Description-Papers/RescueSimulation/Virtual-Robot-Competition/RoboCup_2016_RescueS_Virtual_TDP_SOS.pdf) if you use the code in your work.*
[Taher Ahmadi](https://ceit.aut.ac.ir/~taher), [Sajad Azami](https://ceit.aut.ac.ir/~azami)


---
# [Team SOSvr](https://sosvr.github.io) Virtual Robot Simulation Base Code 2.0

This is our base code that can be used to build different robots for performing different tasks and simulate them in 3D with Gazebo. We have used ROS for developing our robot and used P3AT as the robot's model.
For setting up this robot refer to the **usage** section.

## Usage
We assume you have an **Ubuntu 16.04** machine set up. Follow these steps to bring up the robot: 

## Installing Ros Indigo
First you have to install **ROS kinetic**:

### Set up your sources.list
```
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
```
### Set up your keys
```
sudo apt-key adv --keyserver hkp://ha.pool.sks-keyservers.net:80 --recv-key 421C365BD9FF1F717815A3895523BAEEB01FA116
```
### Installation
```
sudo apt-get update
sudo apt-get install ros-kinetic-desktop-full
```
## Installing Gazebo
For using 3D simulated environment we use Gazebo7:
```
sudo apt-get install gazebo7
``` 
## Install Some ROS Packages
This packages are needed for the code to be maked and compiled:
### Controller Manager
```
sudo apt-get install ros-kinetic-controller-manager 
```
### Joy
```
sudo apt-get install ros-kinetic-joy
```
### Gmapping
```
sudo apt-get install ros-kinetic-gmapping
```
### Move Base
```
sudo apt-get install ros-kinetic-move-base
```
### Hector Mapping
```
sudo apt-get install ros-kinetic-hector-mapping
```
## Compiling and Running
Here we should first create a catkin workspace and compile and run our code. Follow these steps to finally see the result:

## Creating a workspace
Use these commands to create a catkin workspace: (here we name it *catkin_ws*)  
```
source /opt/ros/kinetic/setup.bash
mkdir -p ~/catkin_ws/src
cd ~/catkin_ws/src
catkin_init_workspace
```
Then copy the contents of **src** folder from here to the **src folder of your workspace**.

### Compiling the code
Assuming you're in the home directory and your catkin workspace folder is named **catkin_ws** use these commands:
```
cd catkin_ws
catkin_make
``` 
### Source your project shell environment variables :
Run this command before run each 
```
source ./devel/setup.bash
```
or (if using zsh shell )
```
source ./devel/setup.zsh
```


## Running the code:
Use these commands to bring up the 3D environment with the robot spawned in it:
(Run each in seprate terminal session and dont forget to run the command from previous step before each)
```
roslaunch setup p3at_main.launch


```
Then Gazebo should be up and running with robot spwaned in it :)

## Using SOSVR Controller to drive the robot:
connect the joystick then Run:
```
roslaunch setup utility.launch
```
but you still can't drive the robot unless you run:
```
rqt --force-discover
```
choose the "SOSVR Controller" from Plugins menu then select the robot1 and press play button.
press A & X buttons at the same time for speed mode, now Enjoy your ride :)



