#!/usr/bin/env python

import roslib;
import rospy;
import tf;
import math;
from aut_exploration.msg import *;
from aut_exploration.srv import *;
from geometry_msgs.msg import *;
from nav_msgs.msg import *;
from std_msgs.msg import Header;
from tf import TransformListener;
#from rail_object_detector.msg import *;
merged_map=None;
map_width=0;
map_height=0;

def setMap(rawMap):
    global merged_map;
    merged_map=[];
    for i in range(0,map_height):
        merged_map.insert(i,rawMap.data[i*map_width:(i+1)*map_width]);

def start_listening():
    print ("Reading the merged map data for exploration server");
    rospy.Subscriber("/map", OccupancyGrid, setMap);


def find_far_goal1(req):
    if (req.request_type=="goal"):
        a="taher";
        if (a=="javadi"):
            k=FarGoalResponse();
            k.goal_y=0; #this two numbers should be the x and y of the goal that the server has chosen
            k.goal_x=0;
            k.response_type="yourgoal";
            return k;
        elif (a=="azami"):

    elif (req.request_type=="new_goal"):
        pass;

    return FarGoalResponse();

def start_server():
    rospy.init_node("exploration server");

    global map_width;
    global map_height;

    map_width=rospy.get_param("map_width",default_value=0);
    map_height=rospy.get_param("map_height",default_value=0);

    start_listening();
    rospy.loginfo("starting the exploration server");

    s = rospy.Service("/sos1/request_fargoal", FarGoal, find_far_goal1);
    s = rospy.Service("/sos2/request_fargoal", FarGoal, find_far_goal2);
    s = rospy.Service("/sos3/request_fargoal", FarGoal, find_far_goal3);
    s = rospy.Service("/sos4/request_fargoal", FarGoal, find_far_goal4);
    rospy.spin();

if __name__ == '__main__':
    start_server();
