#!/usr/bin/env python
import rospy
import sys

sys.path.append("/home/user/workspaces/communication_node/src/gazebo_plugins/scripts")
from getInfo import GetInfo

if __name__ == "__main__":
    rospy.init_node("test_node")
    a = GetInfo()
    print a.request(robot1="asphalt_plane", robot2="asphalt_plane_1")[1]
    print "this was the distance that you expected"
