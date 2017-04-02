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

nav_msgs::OccupancyGrid mapdata;

nav_msgs::Odometry mydata;




void callBack(nav_msgs::Odometry odomdata){

  mydata=odomdata;

}
void mapcallBack(const nav_msgs::OccupancyGrid mapraw){
  mapdata=mapraw;

}

int main(int argc, char** argv){
  ros::init(argc, argv, "odometry_publisher");
  std::string ns=argv[1];

  mapdata.header.frame_id="hi";
  ros::NodeHandle n;
  std::string maptopic="/"+ns+"/map";//move_base/local_costmap/costmap";
  ros::Subscriber map_subscriber = n.subscribe(maptopic, 5,mapcallBack);
//  ros::Publisher polygonPublisher= n.advertise<geometry_msgs::PolygonStamped>("sos1/polygon",10);
  //  std::string robotname="/"+ns+"/odom";
  //  ros::Subscriber odom_pub = n.subscribe(robotname, 50,callBack);
  //  tf::TransformBroadcaster odom_broadcaster;
  //  ros::Time current_time;
  //
  //  geometry_msgs::TransformStamped odom_trans;
  //  geometry_msgs::TransformStamped odom_trans_two;
  //
  //   robotname=ns+"/odom";
  //  odom_trans.header.frame_id = robotname;
  //  robotname=ns+"/base_link";
  //
  //  odom_trans.child_frame_id = robotname;
  //
  // robotname=ns+"/odom";
  //  odom_trans_two.header.frame_id = "map";
  //  odom_trans_two.child_frame_id = robotname;
  ros::Rate r(10);
  int qw=0;
  while(n.ok()){

    ros::spinOnce();
  //  if(mapdata.header.frame_id=="hi")continue;
    // ROS_INFO("this is my map width -> %d   height -> %d    %s    seq->  %d \n",mapdata.info.width,mapdata.info.height,mapdata.header.frame_id.c_str(),mapdata.header.seq);
    // ROS_INFO("x= %f y=%f z=%f \n",mapdata.info.origin.position.x,mapdata.info.origin.position.y,mapdata.info.origin.position.z);
    // std::vector<int> v;
    int j,i,sum,k,l;
    std::vector<int8_t> a=mapdata.data;
    int q=sqrt(a.size());
    if(q!=qw){
     qw=q;
     ROS_INFO("howdy bitch howdy bitch howdy bitch\n howdy bitch howdy\n bitch %d   \n ",qw);


    }
    // for(j=1;j<(q);j++){
    //
    //   for(i=1;i<(q);i++){
    //     if(a[i+j*(q)]>70)ROS_INFO("%d  ----- %d   %d",i,j,q);
    //     else{
    //       // sum=0;
    //       // for(l=-1;l<2;l++){
    //       //   for (k=-1;k<2;k++){
    //       //     if(k==l && k==0)continue;
    //       //     if(a[i+k+(j+l)*900]<0)sum++;
    //       //     else sum--;
    //       //   }
    //       // }
    //       //
    //       // if(sum>-4 && sum<2) v.push_back(i+j*900);
    //
    //     }
    //
    //   }
    //
    //
    // }
     i=0;
    // geometry_msgs::PolygonStamped input_;
    // input_.header.frame_id = "map";
    //
    //  for(i=0;i<v.size();i++){
    //      geometry_msgs::PointStamped point;
    //      j=v[i]/900;
    //
    //      point.point.x=(v[i]%900)*0.05;
    //      point.point.y=j*0.05;
    //      point.point.z=0;
    //      point.header.frame_id="map";
    //      point.header.stamp=ros::Time::now();
    //      point.header.seq=i;
    //      if(i==0){
    //        input_.header = point.header;
    //        input_.polygon.points.push_back(costmap_2d::toPoint32(point.point));
    //
    //      }else{
    //      input_.header.stamp = ros::Time::now();
    //      input_.polygon.points.push_back(costmap_2d::toPoint32(point.point));
    // }
    //
    //  }
    //
    // polygonPublisher.publish(input_);

    // current_time = ros::Time::now();
    //
    //
    //
    //
    //
    // odom_trans.header.stamp = current_time;
    // odom_trans_two.header.stamp = current_time;
    //
    //
    //
    //
    // odom_trans.transform.translation.x = mydata.pose.pose.position.x;
    // odom_trans.transform.translation.y = mydata.pose.pose.position.y;
    // odom_trans.transform.translation.z =mydata.pose.pose.position.z;
    // odom_trans.transform.rotation=mydata.pose.pose.orientation;
    //
    //  //khob gmapping aslan be in node niazy nadare gampping map be odom ro mide model odom be base ro
    //  //vali hector age odom base ro model bede  va map odom ro kamel 0 bedim 90 darsad oke
    //  //khob baad az koli dardesar natije ine ke fek konam fek konam fek konam shayad (in faghat ye ehtemal) map be odom dar vaghe bordar makanie ke ebtedash markaze
    //  // mokhtasate vali entehash noghte vasate base linke yani amalan nemitone bege model dare kodom samt ro negah mikone vali x y z ono moshakhas mikone
    //  // va baad odom be base jahat giri ro
    // odom_trans_two.transform.translation.x =0;// mydata.pose.pose.position.x;
    // odom_trans_two.transform.translation.y =0;// mydata.pose.pose.position.y;
    // odom_trans_two.transform.translation.z =0;// mydata.pose.pose.position.z;
    // odom_trans_two.transform.rotation.x=0;//mydata.pose.pose.orientation;
    // odom_trans_two.transform.rotation.y=0;
    // odom_trans_two.transform.rotation.z=0;
    // odom_trans_two.transform.rotation.w=1;
    //
    //
    //
    //
    //
    //
    // //odom_broadcaster.sendTransform(odom_trans);
    // odom_broadcaster.sendTransform(odom_trans_two);
    //


    r.sleep();
  }
}
