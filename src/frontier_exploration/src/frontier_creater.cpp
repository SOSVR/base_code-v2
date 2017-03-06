#include <ros/ros.h>
#include <actionlib/client/simple_action_client.h>
#include <costmap_2d/costmap_2d_ros.h>
#include <costmap_2d/costmap_2d.h>
#include <string>
#include <frontier_exploration/ExploreTaskAction.h>
#include <frontier_exploration/ExploreTaskActionGoal.h>
#include <geometry_msgs/PolygonStamped.h>
#include <geometry_msgs/PointStamped.h>
#include <costmap_2d/footprint.h>
#include <tf/transform_listener.h>

#include <ros/wall_timer.h>
#include <time.h>
#include <move_base_msgs/MoveBaseAction.h>

namespace my_namespace{



class frontier_creater{

private:

    ros::NodeHandle nh_;
    ros::NodeHandle private_nh_;
    ros::Publisher point_;

    geometry_msgs::PolygonStamped input_;


    /**
     * @brief Publish markers for visualization of points for boundary polygon.
     */

    /**
     * @brief Build boundary polygon from points received through rviz gui.
     * @param point Received point from rviz
     */
    void pointCb(int pose){
      sleep(3);

        float points [9]={0.002,pose,pose,-pose,pose,-pose,-pose,pose,-pose};

        for(int i=1;i<5;i++){

        geometry_msgs::PointStamped point;
          point.point.x=points[i];
          point.point.y=points[2*i];
          point.point.z=points[0];
          point.header.frame_id="map";
          point.header.stamp=ros::Time::now();
          point.header.seq=i-1;
          point_.publish(point);
          if(i==1){
            input_.header = point.header;
            input_.polygon.points.push_back(costmap_2d::toPoint32(point.point));
          }
          else{
            input_.polygon.points.push_back(costmap_2d::toPoint32(point.point));
            input_.header.stamp = ros::Time::now();
          }

          sleep(1);
               }

                 geometry_msgs::PointStamped point;
                   point.point.x=1;
                   point.point.y=-1;
                   point.point.z=points[0];
                   point.header.frame_id="map";
                   point.header.stamp=ros::Time::now();
                   point.header.seq=5;

                 actionlib::SimpleActionClient<frontier_exploration::ExploreTaskAction> exploreClient("explore_server", true);
                 exploreClient.waitForServer();
                 frontier_exploration::ExploreTaskGoal goal;
                 goal.explore_center = point;
                 goal.explore_boundary = input_;
                 exploreClient.sendGoal(goal);
    }

public:

    /**
     * @brief Constructor for the client.
     */
    frontier_creater(int pose) :
        nh_(),
        private_nh_("~")
    {
        input_.header.frame_id = "map";
        point_ = nh_.advertise<geometry_msgs::PointStamped>("/clicked_point", 5);
        pointCb(pose);
    }

};

}

int main(int argc, char** argv)
{
    ros::init(argc, argv, "frontier_creater_node");
    std::string s=argv[1];
    int myNr =  atoi(s.c_str());
    my_namespace::frontier_creater fc(myNr);
    ros::spin();
    return 0;
}
