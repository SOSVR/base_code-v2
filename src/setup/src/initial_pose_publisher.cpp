#include <ros/ros.h>
#include <std_msgs/Header.h>
#include <iostream>
#include <stdlib.h> // atof
#include <string>
#include <geometry_msgs/PoseWithCovarianceStamped.h>


int main(int argc, char** argv){
  ros::init(argc, argv, "initial_pose_publisher");
  std::string ns=argv[1];
  std::string n1=argv[2];
  std::string n2=argv[3];
  ros::NodeHandle n;
  std::string topic="/"+ns+"/in_pose";

  ros::Publisher posepublisher= n.advertise<geometry_msgs::PoseWithCovarianceStamped>(topic,10);

  float a,b;
  a=atof(n1.c_str());
  b=atof(n2.c_str());
  geometry_msgs::PoseWithCovarianceStamped c;
  c.header.frame_id="map";
  c.header.seq=0;
  c.header.stamp=ros::Time::now();

  c.pose.pose.position.x=a;
  c.pose.pose.position.y=b;
  c.pose.pose.position.z=0;
  c.pose.pose.orientation.x=0;
  c.pose.pose.orientation.y=0;
  c.pose.pose.orientation.z=0;
  c.pose.pose.orientation.w=1;
   for(int k=0;k<36;k++){
     c.pose.covariance[k]=0;
   }
   c.pose.covariance[0]=0.25;
   c.pose.covariance[7]=0.25;
   c.pose.covariance[35]=0.06853891945200942;
  ros::Rate r(2);
   while(n.ok()){
     ros::spinOnce();
     c.header.stamp=ros::Time::now();
   posepublisher.publish(c);

 r.sleep();
}
  return 0;}
