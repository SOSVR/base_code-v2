#!/usr/bin/env python

import rospy;
import math;
import threading;
import numpy as np;
from nav_msgs.srv import GetPlan ,GetPlanRequest;
from nav_msgs.msg import Path , OccupancyGrid, Odometry;
from geometry_msgs.msg import Point , PoseStamped
from std_msgs.msg import Bool;
import roslib;
import actionlib;
from actionlib_msgs.msg import *;
from move_base_msgs.msg import *;


name_space="robot1";
robot_number=0;
number_of_robots=0;
######################
merged_map=None;
#####################
map_publisher=None;
goal_publisher=None;
#############
odom_subscriber=None;
robot_x=0;
robot_y=0;
#################
#################
move_client_=None
move_client_goal_=None;
goal_pose=PoseStamped();
current_goal_status = 0 ; # goal status--- PENDING=0--- ACTIVE=1---PREEMPTED=2--SUCCEEDED=3--ABORTED=4---REJECTED=5--PREEMPTING=6---RECALLING=7---RECALLED=8---LOST=9
move_base_status_subscriber=None;
#########################

################################################
################################################
def callback_goal_status(data,data2):
    global current_goal_status;
    current_goal_status=True;
    return;
    if len(data.status_list)==0 :
        return;
    current_goal_status = data.status_list[len(data.status_list) - 2].status;

def move_base_tools():
    global move_client_goal_;
    global move_client_;
    global name_space;
    global move_base_status_subscriber;
    move_client_=actionlib.SimpleActionClient("/"+name_space+"/move_base", MoveBaseAction);
    move_client_goal_=MoveBaseGoal();
    print(name_space,"move base tools are ok")
    #move_base_status_subscriber=rospy.Subscriber("/"+name_space+"/move_base/status", GoalStatusArray, callback_goal_status);


################################################
################################################################################################
################################################




def send_goal(goal_x,goal_y):
    global other_robots_list,goal_publisher;
    global name_space;
    global move_client_;
    global move_client_goal_;
    global goal_pose;
    global my_current_goal;
    my_current_goal=Point(goal_x,goal_y,0.0);

        # set goal
    goal_pose.pose.position.x = goal_x;
    goal_pose.pose.position.y = goal_y;
    goal_pose.pose.orientation.w = 1.0;
    goal_pose.pose.orientation.z = 0;
    goal_pose.header.frame_id = "/map";
    goal_pose.header.stamp = rospy.Time.now();
        # send goal
    move_client_.cancel_goals_at_and_before_time(rospy.Time.now());
    move_client_goal_.target_pose=goal_pose;
    rospy.sleep(0.5);

    #move_client_.send_goal_and_wait(goal=move_client_goal_,execute_timeout = rospy.Duration(300),preempt_timeout = rospy.Duration(1));
    move_client_.send_goal(goal=move_client_goal_,done_cb=callback_goal_status);
    print(name_space,"sent goal");
    goal_pose.header.seq =goal_pose.header.seq+1 ;
################################################
################################################
def map_callback(map_data):
    global merged_map,merged_map_lock;
    global other_robots_list;
    global map_publisher;
    global map_pub_counter,map_pub_frequnecy;
    merged_map=map_data;


def odom_callback(odom_data):
    global robot_x,robot_y;
    robot_x=odom_data.pose.pose.position.x;
    robot_y=odom_data.pose.pose.position.y;
################################################
################################################


def main():
    global name_space,robot_number,number_of_robots;
    global merged_map,goals_list,other_robots_list;
    global goal_publisher,a_star;
    global map_publisher,odom_subscriber;
    global checking_goals_subscriber,checking_goals_publisher;
    rospy.init_node("auto_move_base");
    name_space = rospy.get_param("namespace", default="robot1");
    move_base_tools();
    map_subscriber=rospy.Subscriber("/"+name_space+"/map", OccupancyGrid, map_callback);
    odom_subscriber=rospy.Subscriber("/"+name_space+"/odom", Odometry, odom_callback);
    send_goal(-10,-15);

    rospy.spin();

if __name__ == '__main__':
    main();
