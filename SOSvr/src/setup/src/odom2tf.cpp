#include <ros/ros.h>
#include <tf/transform_broadcaster.h>
#include <nav_msgs/Odometry.h>
#include <string>
#include <iostream>

nav_msgs::Odometry mydata;
void callBack(nav_msgs::Odometry odomdata){

  mydata=odomdata;

}



int main(int argc, char** argv){
  ros::init(argc, argv, "odometry_publisher");
  std::string ns=argv[1];
  std::string robotname="/"+ns+"/odom";


  ros::NodeHandle n;
  ros::Subscriber odom_pub = n.subscribe(robotname, 50,callBack);
  tf::TransformBroadcaster odom_broadcaster;
  ros::Time current_time;

  geometry_msgs::TransformStamped odom_trans;
  geometry_msgs::TransformStamped odom_trans_two;

   robotname=ns+"/odom";
  odom_trans.header.frame_id = robotname;
  robotname=ns+"/base_link";

  odom_trans.child_frame_id = robotname;

 robotname=ns+"/odom";
  odom_trans_two.header.frame_id = "map";
  odom_trans_two.child_frame_id = robotname;
  ros::Rate r(150);
  while(n.ok()){

    ros::spinOnce();
    current_time = ros::Time::now();





    odom_trans.header.stamp = current_time;
    odom_trans_two.header.stamp = current_time;




    odom_trans.transform.translation.x = mydata.pose.pose.position.x;
    odom_trans.transform.translation.y = mydata.pose.pose.position.y;
    odom_trans.transform.translation.z = mydata.pose.pose.position.z;
    odom_trans.transform.rotation= mydata.pose.pose.orientation;


    odom_trans_two.transform.translation.x =0;// mydata.pose.pose.position.x;
    odom_trans_two.transform.translation.y = 0;//mydata.pose.pose.position.y;
    odom_trans_two.transform.translation.z =0;// mydata.pose.pose.position.z;
    odom_trans_two.transform.rotation.x=0;// mydata.pose.pose.orientation;
odom_trans_two.transform.rotation.y=0;
odom_trans_two.transform.rotation.z=0;
odom_trans_two.transform.rotation.w=1;






    odom_broadcaster.sendTransform(odom_trans);
    odom_broadcaster.sendTransform(odom_trans_two);



    r.sleep();
  }
}
