#include <ros/ros.h>
#include <move_base_msgs/MoveBaseAction.h>
#include <actionlib/client/simple_action_client.h>
#include <string>
#include <nav_msgs/Odometry.h>
#include <costmap_2d/footprint.h>
#include <nav_msgs/OccupancyGrid.h>

typedef actionlib::SimpleActionClient<move_base_msgs::MoveBaseAction> MoveBaseClient;
move_base_msgs::MoveBaseGoal goal;
MoveBaseClient *ac;
ros::Subscriber odom_sub,map_sub;
bool flag;
nav_msgs::Odometry mydata;
nav_msgs::OccupancyGrid mapdata;

void odomCallBack(nav_msgs::Odometry odomdata){
  mydata=odomdata;
}


void mapCallBack(const nav_msgs::OccupancyGrid mapraw){
  mapdata=mapraw;
}
void findgoal(){
    flag=false;
    float x,y;
  // in gharare be ma bege ke koja bayad berim bara explore




  send_goal(x,y);



}



void send_goal(float x,float y){
  flag=true;
  goal.target_pose.header.stamp = ros::Time::now();
  goal.target_pose.pose.position.x = x;
  ggoal.target_pose.pose.position.x = y;
  goal.target_pose.pose.orientation.w = 1.0;
  ROS_INFO("Sending goal  %f --%f",x,y);
  ac->sendGoal(goal);
  ac->waitForResult();

  if(ac->getState() == actionlib::SimpleClientGoalState::SUCCEEDED)
    ROS_INFO("Hooray, the base reached (%f --- %f ) \n",x,y);
  else
    ROS_INFO("The base failed to move to %f ---%f for some reason  \n",x,y);
   flag=true;
}



int main(int argc, char** argv){
  ros::init(argc, argv, "simple_navigation_goals");
  ros::NodeHandle n;
  goal.target_pose.header.frame_id = "/map";
  goal.target_pose.header.stamp = ros::Time::now();
  std::string ns=argv[1];
  odom_pub = n.subscribe(ns+"/odom", 10,odomCallBack);
  map_sub = n.subscribe(ns+"/move_base/global_costmap/costmap", 5,mapCallBack);

  //tell the action client that we want to spin a thread by default
  ac=new MoveBaseClient(ns+"/move_base", true);





  //wait for the action server to come up
  while(!ac->waitForServer(ros::Duration(1.0))){
    ROS_INFO("Waiting for the move_base action server to come up \n ");
  }

    findgoal();

  return 0;
}
