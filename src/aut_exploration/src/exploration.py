#!/usr/bin/env python

import roslib;
import rospy;
import smach;
import smach_ros;
import actionlib;
import tf;
import math
from aut_exploration.msg import *;
from geometry_msgs.msg import *;
from nav_msgs.msg import *;
from actionlib_msgs.msg import *;
from move_base_msgs.msg import *;
from smach_ros import ServiceState;
from std_msgs.msg import Header;
from tf import TransformListener;


move_base_cancel=None;
GCostmap_data = None;
robotnamespace = None;
Odom_data = None;
current_victim_status=None;
current_goal_status = 0 ; # goal status
# PENDING=0
# ACTIVE=1
# PREEMPTED=2
# SUCCEEDED=3
# ABORTED=4
# REJECTED=5
# PREEMPTING=6
# RECALLING=7
# RECALLED=8
# LOST=9

def cancel_publisher():
    global move_base_cancel;
    move_base_cancel=rospy.Publisher(robotnamespace+"/move_base/cancel",GoalID,10);


def in_range(x, y, w, z):
    return math.sqrt((x - w) ** 2 + (y - z) ** 2);


def setOdom(rawodomdata):
    Odom_data = rawodomdata;


def setMap(costmap_data):
    GCostmap_data = costmap_data;


def PxCalculator(mapdata):
    sum = 0;
    for i in range(0, len(mapdata)):
        if mapdata[i] >= 0:
            sum += 1;
        else:
            sum -= 1;
    final_sum = (sum + len(mapdata)) / (2 * len(mapdata)) * 100;
    return final_sum;



# subscriber method callback from /move_base/status
def callback_goal_status(data):
    global current_goal_status
    current_goal_status = data.status_list[len(data.status_list) - 1].status


# subscriber method from /move_base/status
def listener_goal_status():
    rospy.Subscriber((robotnamespace + "/move_base/status"), GoalStatusArray, callback_goal_status)


def Block_chosser(mapdata):
    # global current_goal_status
    # listener_goal_status()

    length = int(math.sqrt(len(mapdata)));
    dividor3 = int(length / 3);
    blocks = [];
    a = 0;
    for i in range(0, length, dividor3):
        for k in range(0, length, dividor3):
            blocks[a] = [];
            for j in range(0, dividor3):
                blocks[a].extend(mapdata[i * length + j * length + k:i * length + j * length + k + dividor3 - 1]);
    a += 1;
    minPX = PxCalculator(blocks[0]);
    minIndex = 0;
    for w in range(1, 9):
        if PxCalculator(blocks[w]) < minPX:
            minPX = PxCalculator(blocks[w]);
            minIndex = w;

    if minPX > 75:
        return -1;
    else:
        return minIndex;




class Point():
    def __init__(self, xVector, yVector):
        self.type = "Point";
        self.resault = None;
        self.x = xVector;
        self.y = yVector;



class Block():

    def __init__(self, center, tl, tr, br, bl, matrix):
        self.type = "Block";
        self.center = center;
        self.topLeft = tl;
        self.topRight = tr;
        self.bottomRight = br;
        self.bottomLeft = bl;
        self.matrix = matrix;



# define state Chose_block
##############################3
##############################

class Chose_block(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=["block_choosed", "no_block_found"], input_keys=["CB_input"],
                             output_keys=["CB_output"]);
        self.counter = 0;
        self.block = None;
        self.center = None;
        self.topLeft = None;
        self.topRight = None;
        self.bottomRight = None;
        self.bottomLeft = None;

    def Calculations(self):
        rospy.loginfo("calculationg");
        # our code
        # goes in this
        # commented lines and points are created
        #
        lenght = GCostmap_data.info.width * 10;
        x = (Odom_data.pose.pose.position.x - GCostmap_data.info.origin.position.x) * 10;
        y = (Odom_data.pose.pose.position.y - GCostmap_data.info.origin.position.y) * 10;

        if x < 275:
            x_gc = 0;
        elif x > lenght - 275:
            x_gc = int(lenght - 275);
        else:
            x_gc = int(x) - 270;
        if y < 275:
            y_gc = 0;
        elif y > lenght - 275:
            y_gc = int(lenght - 275);
        else:
            y_gc = int(y) - 270;

        Cell = [];
        for i in range(0, 180):
            Cell.extend(GCostmap_data.data[(y_gc + i) * lenght:(1 + y_gc + i) * lenght]);
        block_index = Block_chosser(Cell);
        if block_index == -1:
            return "conntact the master";
        else:
            cx = x_gc / 10.0 + (block_index % 3) * 18.0 + 9.0;
            cy = y_gc / 10.0 + (int(block_index / 3)) * 18.0 + 9.0;
            self.center = Point(cx, cy);
            self.topLeft = Point(cx - 7, cy + 7);
            self.topRight = Point(cx + 7, cy + 7);
            self.bottomRight = Point(cx + 7, cy - 7);
            self.bottomLeft = Point(cx - 7, cy - 7);
            self.block = Block(self.center, self.topLeft, self.topRight, self.bottomRight, self.bottomLeft,
                               Cell[block_index]);

    def execute(self, userdata):
        rospy.loginfo("Executing state Chose_block");
        a = self.Calculations();
        if a == "conntact the master":
            return "no_block_found";
        else:
            userdata.CB_output = self.block;
            return "block_choosed";


# define state Explore_Center
##############################3
##############################
class Explore_Block(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=["stucked", "exploration_completed", "exploration_failed", "point_reached"],
                             input_keys=["EB_input"], output_keys=["EB_output"]);
        self.block = None;
        self.status = None;
        self.points = None;
        self.count = 0;

    def odomCallback(data):
        pass;

    def move_to_goal(self, pos_x, pos_y, pos_z=0, ornt_w=1, ornt_x=0, ornt_y=0, ornt_z=1):
        # Simple Action Client
        sac = actionlib.SimpleActionClient(robotnamespace + "/move_base", MoveBaseAction);

        # create goal
        goal = MoveBaseGoal();

        # set goal
        goal.target_pose.pose.position.x = pos_x;
        goal.target_pose.pose.position.y = pos_y;
        goal.target_pose.pose.orientation.w = ornt_w;
        goal.target_pose.pose.orientation.z = ornt_z;
        goal.target_pose.header.frame_id = (robotnamespace + "/odom");
        goal.target_pose.header.stamp = rospy.Time.now();

        # start listener
        sac.wait_for_server();

        # send goal
        sac.send_goal(goal);
        odom_temp = Odom_data;
        rate = rospy.Rate(3);  # 10hz
        i = 0;
        while not rospy.is_shutdown():
            if odom_temp.pose.pose.position.x == Odom_data.pose.pose.position.x and odom_temp.pose.pose.position.y == Odom_data.pose.pose.position.y:
                i += 1;
            else:
                odom_temp = Odom_data;
            if current_victim_status=="victim detected" :
                a = rospy.Publisher("move_base/cancel", GoalID, queue_size=10);
                a.publish(GoalID());
                rospy.sleep(30.0);
                goal.target_pose.header.stamp = rospy.Time.now();
                sac.send_goal(goal);
            elif current_goal_status==3 or current_goal_status==4 or current_goal_status==5 or current_goal_status==9:
                px=PxCalculator(self.matrix);
                if px >75 :
                    self.status="fully explored";
                    return;
                else:
                    self.status="not explored yet";
                    return ;
            elif i==36 :
                px = PxCalculator(self.matrix);
                if px > 75:
                    self.status = "fully explored";
                    return;
                else:
                    self.status = "not explored yet";
                    return;

            rate.sleep();


            # finish

            # print result
            # goal_result = sac.get_result()

    def execute(self, userdata):
        rospy.loginfo("Executing state Explore_Center");
        a = userdata.EB_input;
        userdata.EB_output=a;
        if a.type == "Block" and self.count == 0:
            self.block = a;
            self.points = [ (a.center),(a.topLeft),(a.topRight),(a.bottomRight),(a.bottomLeft)];
            self.move_to_goal(self.points[self.count].x,self.points[self.count].y);
        elif a.type == "Block" and self.count > 0:
            self.move_to_goal(self.points[self.count].x,self.points[self.count].y);
            self.count += 1;
            if self.count > 4:
                if self.status == "not explored yet":
                    self.status = "exploration failed";
                self.count = 0;


        if self.status == "fully explored":
            return "exploration_completed";
        elif self.status == "exploration failed":
            return "exploration_failed";
        elif self.status == "not explored yet":
            return "point_reached";
        else:
            return "exploration_completed";


# define state Conntact_master
##############################3
##############################


class Conntact_master(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=["goal_received", "NOT_received", "map_fully_explored"],
                             input_keys=["CM_input"], output_keys=["CM_output"]);
        self.goal = None;
        self.pub=rospy.Publisher("requet_of_goal",Odometry,10);
        self.sub=rospy.Subscriber("respans_from_master",Odometry,self.sub_callBack);
        self.goal=None;

    def sub_callBack(self,data):
        rospy.loginfo("sub_callBack");
        self.goal=Point(data.pose.pose.position.x,data.pose.pose.position.y);
        if data.pose.pose.position.z==10 :
            self.goal.resault="found";




    def execute(self, userdata):
        rospy.loginfo("Executing state Conntact_master");
        r=rospy.Rate(1);
        i=0;
        a = "taher";
        while not rospy.is_shutdown() :

            if i>20 :
                userdata.CM_output=userdata.CM_output;
                a=None;
                self.goal=None;
                break;
            elif self.goal==None :
                i+=;
            else:
                userdata.CM_output=self.goal;
                if self.goal.resault=="found":
                     a="goal received"
                else:
                    a="map explored";
                self.goal=None;
                break;
            r.sleep();


        if a == "goal received":
            return "goal_received";
        elif a == "map explored":
            return "map_fully_explored";
        else:
            return "NOT_received";


##############################3
##############################



class GOTO_Goal(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=["goal_reached", "stucked", "failed_toMOVE"], input_keys=["GG_input"],
                             output_keys=["GG_output"]);
        self.goal = None;

    def Calculations(self):
        rospy.loginfo("calculationg");

    def execute(self, userdata):
        rospy.loginfo("Executing state GOTO_Goal");

        a = "taher";
        if a == "javadi":
            return "goal_reached";
        elif a == "azami":
            return "stucked";
        else:
            return "failed_toMOVE";


# define state Request_different_goal
##############################3
##############################



class a_simple_state(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=["shuting_down", "comon"]);

    def Calculations(self):
        rospy.loginfo("calculationg");

    def execute(self, userdata):
        rospy.loginfo("Executing state Request_different_goal");
        a = "taher";
        if a == "javadi":
            return "shuting_down";
        else:
            return "comon";


# our main function
##############################3
##############################





def main():
    rospy.init_node('smach_example_state_machine');

    Odom_topic = "/%s/odom" % (robotnamespace);
    rospy.Subscriber(Odom_topic, Odometry, setOdom);
    global_costmap_topic = "/%s/move_base/global_costmap/costmap" % (robotnamespace);
    rospy.Subscriber(global_costmap_topic, OccupancyGrid, setMap);

    # Create the top level SMACH state machine
    sm_exploration = smach.StateMachine(outcomes=["hold", "shut_down"]);

    # Open the container
    with sm_exploration:
        smach.StateMachine.add("Chose_block", Chose_block(),
                               transitions={"block_choosed": "Explore_Block", "no_block_found": "Conntact_master"},
                               remapping={"CB_input": "passing_data", "CB_output": "passing_data"});
        smach.StateMachine.add("Explore_Block", Explore_Block(),
                               transitions={"point_reached": "Explore_Block", "exploration_failed": "recovery",
                                            "exploration_completed": "Chose_block", "stucked": "Chose_block"},
                               remapping={"EB_input": "passing_data", "EB_output": "passing_data"});
        smach.StateMachine.add("Conntact_master", Conntact_master(),
                               transitions={"map_fully_explored": "hold", "goal_received": "GOTO_Goal",
                                            "NOT_received": "Conntact_master"},
                               remapping={"CM_input": "passing_data", "CM_output": "passing_data"});
        smach.StateMachine.add("GOTO_Goal", GOTO_Goal(),
                               transitions={"goal_reached": "Chose_block", "stucked": "Conntact_master",
                                            "failed_toMOVE": "recovery"},
                               remapping={"GG_input": "passing_data", "GG_output": "passing_data"});

        # Create the sub SMACH state machine
        sm_recovery = smach.StateMachine(outcomes=["recovery_completed", "recovery_failed"]);

        # Open the container
        with sm_recovery:
            # Add states to the container

            smach.StateMachine.add("simple_state", a_simple_state(),
                                   transitions={"shuting_down": "recovery_failed", "comon": "recovery_completed"});

        smach.StateMachine.add("recovery", sm_recovery,
                               transitions={"recovery_failed": "shut_down", "recovery_completed": "Chose_block"});

        # Execute SMACH plan
    aut_explore = sm_exploration.execute();




if __name__ == '__main__':
    robotnamespace = rospy.get_param("namespace");
    main();