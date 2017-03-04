#include <ros/ros.h>
#include <actionlib/client/simple_action_client.h>
#include <costmap_2d/costmap_2d_ros.h>
#include <costmap_2d/costmap_2d.h>
#include <string>

#include <geometry_msgs/PolygonStamped.h>
#include <geometry_msgs/PointStamped.h>
#include <costmap_2d/footprint.h>
#include <tf/transform_listener.h>

#include <ros/wall_timer.h>

#include <move_base_msgs/MoveBaseAction.h>

namespace my_namespace{



class frontier_creator{

private:

    ros::NodeHandle nh_;
    ros::NodeHandle private_nh_;

    geometry_msgs::PolygonStamped input_;


    /**
     * @brief Publish markers for visualization of points for boundary polygon.
     */

    /**
     * @brief Build boundary polygon from points received through rviz gui.
     * @param point Received point from rviz
     */
    void pointCb(int pose){

        int points [9]={0,pose,pose,-pose,pose,-pose,-pose,pose,-pose};

        for(int i=1;i<5;i++){

        geometry_msgs::PointStamped point;
          point.point.x=points[i];
          point.point.y=points[2*i];
          point.point.z=points[0];
          point.header.frame_id="map";
          point.header.stamp=ros::Time::now();
          point.header.seq=i;
          if(i==1){
            input_.header = point.header;
            input_.polygon.points.push_back(costmap_2d::toPoint32(point.point));
          }
          else{
            input_.polygon.points.push_back(costmap_2d::toPoint32(point.point));
            input_.header.stamp = ros::Time::now();
          }

                 }

                 actionlib::SimpleActionClient<frontier_exploration::ExploreTaskAction> exploreClient("explore_server", true);
                 exploreClient.waitForServer();
                 frontier_exploration::ExploreTaskGoal goal;
                 goal.explore_center = *point;
                 goal.explore_boundary = input_;
                 exploreClient.sendGoal(goal);





        if(waiting_for_center_){
            //flag is set so this is the last point of boundary polygon, i.e. center

            if(!pointInPolygon(point->point,input_.polygon)){
                ROS_ERROR("Center not inside polygon, restarting");
            }else{
                actionlib::SimpleActionClient<frontier_exploration::ExploreTaskAction> exploreClient("explore_server", true);
                exploreClient.waitForServer();
                ROS_INFO("Sending goal");
                frontier_exploration::ExploreTaskGoal goal;
                goal.explore_center = *point;
                goal.explore_boundary = input_;
                exploreClient.sendGoal(goal);
            }
            waiting_for_center_ = false;
            input_.polygon.points.clear();

        }else if(input_.polygon.points.empty()){
            //first control point, so initialize header of boundary polygon

            input_.header = point->header;
            input_.polygon.points.push_back(costmap_2d::toPoint32(point->point));

        }else if(input_.header.frame_id != point->header.frame_id){
            ROS_ERROR("Frame mismatch, restarting polygon selection");
            input_.polygon.points.clear();

        }else if(input_.polygon.points.size() > 1 && pointsNearby(input_.polygon.points.front(), point->point,
                                                                    average_distance*0.1)){
            //check if last boundary point, i.e. nearby to first point

            if(input_.polygon.points.size() < 3){
                ROS_ERROR("Not a valid polygon, restarting");
                input_.polygon.points.clear();
            }else{
                waiting_for_center_ = true;
                ROS_WARN("Please select an initial point for exploration inside the polygon");
            }

        }else{

            //otherwise, must be a regular point inside boundary polygon
            input_.polygon.points.push_back(costmap_2d::toPoint32(point->point));
            input_.header.stamp = ros::Time::now();
        }

    }

public:

    /**
     * @brief Constructor for the client.
     */
    frontier_creator(int pose) :
        nh_(),
        private_nh_("~"),
    {
        input_.header.frame_id = "map";
        pointCb(pose);
    }

};

}

int main(int argc, char** argv)
{
    ros::init(argc, argv, "frontier_creator_node");
    std::string s=argv[1];
    int myNr = std::stoi(s);
    my_namespace::frontier_creator fc(myNr);
    ros::spin();
    return 0;
}
