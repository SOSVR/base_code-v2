#include <ros/ros.h>
#include <tf/transform_listener.h>
#include <laser_geometry/laser_geometry.h>

class My_Filter {
     public:
        My_Filter();
        void scanCallback(const sensor_msgs::LaserScan::ConstPtr& scan);
     private:
        ros::NodeHandle node_;
        laser_geometry::LaserProjection projector_;
        tf::TransformListener tfListener_;

        ros::Publisher point_cloud_publisher_;
        ros::Subscriber scan_sub_;
};

My_Filter::My_Filter(){
        scan_sub_ = node_.subscribe<sensor_msgs::LaserScan> ("/sos1/hokuyo", 100, &My_Filter::scanCallback, this);
        point_cloud_publisher_ = node_.advertise<sensor_msgs::PointCloud2> ("/cloud", 100, false);

}

void My_Filter::scanCallback(const sensor_msgs::LaserScan::ConstPtr& scan){
  if(!tfListener_.waitForTransform(
          scan->header.frame_id,
          "/map",
          scan->header.stamp + ros::Duration().fromSec(scan->ranges.size()*scan->time_increment),
          ros::Duration(1.0))){
       return;
    }

    sensor_msgs::PointCloud2 cloud;
    projector_.transformLaserScanToPointCloud("/map", *scan, cloud, tfListener_);
    point_cloud_publisher_.publish(cloud);

}
int main(int argc, char** argv)
{
    ros::init(argc, argv, "my_filter");
    My_Filter filter;
    ros::spin();
    return 0;
}
