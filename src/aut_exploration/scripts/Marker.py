#!/usr/bin/env python


import roslib;
import rospy;
import actionlib;
import tf;
from visualization_msgs.msg import Marker;
from visualization_msgs.msg import MarkerArray;
from geometry_msgs.msg import *;
from nav_msgs.msg import *;
from actionlib_msgs.msg import *;
from std_msgs.msg import Header;
from tf import TransformListener;
from rail_object_detector.msg import Detections;
from rail_object_detector.msg import Object;

markers=[];
marker_counter=0;
pub2=None;
pub=None;
pub3=None;

def mark_location(data_in):
    global markers;
    global marker_counter;
    global pub2;
    marker_counter+=1;
    mark_id=marker_counter;
    x=data_in.x;
    y=data_in.y;

    #when we call this method , it checks the  array of existing markeres with the new marker
    #and if the new marker is not within 4 meters of any of the existing markers
    #the new marker will be added to the arrey and it  will be shown on the rviz

    shape = Marker.CUBE;

    for i in markers:
        if in_range(x,y,i.pose.position.x,i.pose.position.y) < 4 :
            return "invalid";


    marker = Marker()
    marker.header.frame_id = "/map";
    marker.header.stamp = rospy.Time.now();

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

    marker.scale.x = 0.3
    marker.scale.y = 0.3
    marker.scale.z = 0.3

    marker.color.r = 0.0
    marker.color.g = 0.0
    marker.color.b = 1.0
    marker.color.a = 1.0

    marker.lifetime = rospy.Duration()
    markers.insert(len(markers),marker);

    rospy.loginfo(marker);
    pub2.publish(markers);
    return "valid";

    #rate.sleep()
    #while not rospy.is_shutdown():
    #    pub.publish(marker)
    #    rate.sleep()


def alksdflk(a):
        rate = rospy.Rate(0.5);  # 3hz
        while not rospy.is_shutdown():
                pub.publish(a);
                rate.sleep();


if __name__ == '__main__':
    rospy.init_node('Marker_Node');
    pub2 = rospy.Publisher('/visualization_marker_array', MarkerArray, queue_size=100);
    rospy.Subscriber("/victim_detected",Point,mark_location);
    pub = rospy.Publisher("/detector_node/detections", Detections, queue_size=100);
    pub3 = rospy.Publisher("/pointfucker", Point, queue_size=100);
    a= Detections();
    a.header.frame_id = "/map";
    a.header.stamp = rospy.Time.now();
    b=Object();
    b.label="Human" ;          # Object label
    b.probability =90.0;    # Confidence value in recognition
    b.centroid_x =250;      # X pixel value of the centroid of the bounding box
    b.centroid_y =50;      # Y pixel value of the centroid of the bounding box
    b.left_bot_x=230;       # X pixel value of bottom-left corner of bounding box
    b.left_bot_y =40;      # Y pixel value of bottom-left corner of bounding box
    b.right_top_x =270;     # X pixel value of top-right corner of bounding box
    b.right_top_y =60;     # Y pixel value of top-right corner of bounding box
    a.objects=[b,b,b];
    pub.publish(a);
    pub3.publish(Point(1,8,2));
    print ("hi there");
    alksdflk(a);
    rospy.spin();
