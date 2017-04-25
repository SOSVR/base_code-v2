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

def setMap(rawMap):
    global merged_map;
    merged_map=rawMap;


def start_listening():
    print ("Reading the merged map data for exploration server");
    rospy.Subscriber("/map", OccupancyGrid, setMap);


def find_far_goal1(req):
    return FarGoalResponse();

def start_server():
    rospy.init_node("exploration server");
    start_listening();
    rospy.loginfo("starting the exploration server");
    s = rospy.Service("/sos1/request_fargoal", FarGoal, find_far_goal1);
    s = rospy.Service("/sos2/request_fargoal", FarGoal, find_far_goal2);
    s = rospy.Service("/sos3/request_fargoal", FarGoal, find_far_goal3);
    s = rospy.Service("/sos4/request_fargoal", FarGoal, find_far_goal4);
    rospy.spin();


if __name__ == '__main__':
    start_server();
