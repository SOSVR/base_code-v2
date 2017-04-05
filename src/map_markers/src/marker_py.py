#!/usr/bin/env python

import rospy
from visualization_msgs.msg import Marker


def mark_location(x, y, mark_id):
    shape = Marker.CUBE;
    pub = rospy.Publisher('visualization_marker', Marker, queue_size=100)
    rospy.init_node('map_marker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    
    marker = Marker()
    marker.header.frame_id = "/map"
    marker.header.stamp = rospy.Time.now()


    marker.ns = "basic_shapes"
    marker.id = mark_id


    marker.type = shape


    marker.action = Marker.ADD


    marker.pose.position.x = x
    marker.pose.position.y = y
    marker.pose.position.z = 0
    marker.pose.orientation.x = 0.0
    marker.pose.orientation.y = 0.0
    marker.pose.orientation.z = 0.0
    marker.pose.orientation.w = 1.0


    marker.scale.x = 0.5
    marker.scale.y = 0.5
    marker.scale.z = 0.5


    marker.color.r = 0.0
    marker.color.g = 1.0
    marker.color.b = 0.0
    marker.color.a = 1.0

    marker.lifetime = rospy.Duration()


    rospy.loginfo(marker)
    rate.sleep()
    while not rospy.is_shutdown():
        pub.publish(marker)
        rate.sleep()


if __name__ == "__main__":
    mark_location(6, 2, 3)

