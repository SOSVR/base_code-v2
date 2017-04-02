#include <ros/ros.h>
#include <tf/transform_broadcaster.h>
#include <nav_msgs/Odometry.h>
#include <nav_msgs/OccupancyGrid.h>
#include <string>
#include <std_msgs/Header.h>
#include <iostream>
#include <costmap_2d/footprint.h>
#include <vector>
#include <geometry_msgs/PolygonStamped.h>
#include <geometry_msgs/PointStamped.h>
#include <aut_exploration/Block_msgs.h>

nav_msgs::OccupancyGrid mapdata;
std::vector<int8_t> a;
int map_size;
void mapcallBack(const nav_msgs::OccupancyGrid mapraw){
  mapdata=mapraw;

}


void Px_calcultor(){

  a=mapdata.data;
  map_size=sqrt(a.size());
  int* blocks=new int[9];
  int dividor3=map_size/3;
  int i,j,k=0;
  for(i=0;i<map_size;i++){
    for(j=0;j<dividor3;j++){
      if(a[i+j*map_size]>=0)blocks[k]++;
      else blocks[k]--;
    }
    if(i/dividor3<1)k=0;
    else if(1<i/dividor3<2)k=1;
    else if(i/dividor3>2)k=2;
  }

  k=3;

  for(i=0;i<map_size;i++){
    for(j=dividor3;j<2*dividor3;j++){
      if(a[i+j*map_size]>=0)blocks[k]++;
      else blocks[k]--;
    }
    if(i/dividor3<1)k=3;
    else if(1<i/dividor3<2)k=4;
    else if(i/dividor3>2)k=5;
  }


  k=6;

  for(i=0;i<map_size;i++){
    for(j=2*dividor3;j<map_size;j++){
      if(a[i+j*map_size]>=0)blocks[k]++;
      else blocks[k]--;
    }
    if(i/dividor3<1)k=6;
    else if(1<i/dividor3<2)k=7;
    else if(i/dividor3>2)k=8;
  }

   k=0;

  for(i=0;i<9;i++){
    if(blocks[i]<blocks[k])k=i;
  }

}




int main(int argc, char** argv){
  ros::init(argc, argv, "Px_Calcultor");
  std::string ns=argv[1];
  ros::NodeHandle n;

  std::string maptopic="/"+ns+"/move_base/global_costmap/costmap";
  ros::Subscriber map_subscriber = n.subscribe(maptopic, 5,mapcallBack);
  //  ros::Publisher polygonPublisher= n.advertise<geometry_msgs::PolygonStamped>("sos1/polygon",10);
  //  std::string robotname="/"+ns+"/odom";
  //  ros::Subscriber odom_pub = n.subscribe(robotname, 50,callBack);
  //  tf::TransformBroadcaster odom_broadcaster;

  ros::Rate r(1);
  while(n.ok()){

    ros::spinOnce();
    std::vector<int8_t> a=mapdata.data;
    r.sleep();
  }
}
