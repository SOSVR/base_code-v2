
#include <cstdlib>
#include <unistd.h>
#include <stdio.h>
#include <math.h>
#include <ros/ros.h>
#include <sensor_msgs/LaserScan.h>
#include <geometry_msgs/Twist.h>
#include <nav_msgs/Odometry.h>
#include <rail_object_detector/Detections.h>
#include <std_msgs/String.h>
#include <tf/transform_datatypes.h>
#define PI 3.14159265
  std::vector<float> range;
  double dist = -1;
  int robotX = 0;
  int robotY = 0;
  ros::Publisher victPub;
  double yaw_angle = 0;
  
  struct victLocation {
    double x,y;
  };
  std::vector<victLocation> victims;
   void send_message(){
      std_msgs::String vict;
      vict.data = "victim";
      victPub.publish(vict);
    }
    double computeDistance(int middle){
    int one;
    int two;
    if (middle - 3 >= 0)
      one = middle - 3;
    else
      one = middle + 6;
    if (middle + 3 <= 719)
      one = middle + 3;
    else
      one = middle - 6;
    ROS_INFO("distance calculated!  \n");
    return (double)((range[one] + range[two] + range[middle])/3);
  }
  victLocation getVictimLocation(){
    if (dist == -1)
      ROS_INFO("dist = -1 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \n");
    double victX = robotX + dist * cos(yaw_angle*PI / 180);
    double victY = robotY + dist * sin(yaw_angle*PI / 180);
    victLocation vl;
    vl.x = victX;
    vl.y = victY;
    ROS_INFO("victim location is :  \n");
    return vl;
  }
  bool checkVictim(){
      victLocation vl = getVictimLocation();
      for (std::vector<victLocation>::iterator it = victims.begin() ; it != victims.end(); ++it)
          if((( vl.x  < it->x + 0.5)&&( vl.x > it->x - 0.5))&&(( vl.y < it->y + 0.5)&&( vl.y > it->y - 0.5))){
            ROS_INFO("checkVictim resulted false! \n");
            return false;
    }
    ROS_INFO("checkVictim resulted true! \n");
    return true;
  }
  
  void processLaserScanCallback(const sensor_msgs::LaserScan::ConstPtr& scan){
       ROS_INFO("ranges copying! \n");
       range = scan->ranges;
       ROS_INFO("ranges copied! \n");
  }
  void processDetectionsCallback(const rail_object_detector::Detections::ConstPtr& detect){
    if (detect->objects[0].label == "Human"){
      ROS_INFO("object found! \n");
      int xOfVictimFromMiddle = detect-> objects[0].centroid_x - 140;
      int middleBeam = (xOfVictimFromMiddle / 280) * 360 + 360;
      dist = computeDistance(middleBeam);
      if (checkVictim()){
        ROS_INFO("new victim! \n");
        victims.push_back(getVictimLocation());
        send_message();
      }
    }
    else{
      dist = -1;
      ROS_INFO("dist seted on -1 ! \n");  
    }
  }
  void robotPoseInitialCallback(const nav_msgs::Odometry::ConstPtr& msg){
    ROS_INFO("robot location is initialising!  \n");
    robotX = msg->pose.pose.position.x;
    robotY = msg->pose.pose.position.y;
    tf::Pose pose;
    tf::poseMsgToTF(msg->pose.pose, pose);
    yaw_angle = tf::getYaw(pose.getRotation());
    ROS_INFO("robot location is :  \n");
  }
  void firstInit(){
    ros::NodeHandle nh;
    ros::Subscriber scanSub;
    ros::Subscriber victSub;
    ros::Subscriber robotPoseSub;
    scanSub=nh.subscribe<sensor_msgs::LaserScan>("/sos1/base_scan",10,processLaserScanCallback);
    victSub=scanSub=nh.subscribe<rail_object_detector::Detections>("/detector_node/detections",10,processDetectionsCallback);
    robotPoseSub=nh.subscribe<nav_msgs::Odometry>("/sos1/odom",10,robotPoseInitialCallback);
    victPub = nh.advertise<std_msgs::String>("/victim_detected", 10);
    ROS_INFO("firstInit done! \n");
  }
/** needs to be optimised */

 
int main(int argc, char **argv)
{
  ros::init(argc, argv, "position_estimator");
  ros::Time::init();
  ros::Rate pub_rate(20);
  firstInit();
  ROS_INFO("firstInit called! \n");
  while (ros::ok())
  {
    ros::spinOnce();
    pub_rate.sleep();
  }
  exit(0);
  return 0;
}

