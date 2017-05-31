#!/usr/bin/env python

import roslib;
import rospy;
import smach;
import smach_ros;
import actionlib;
import tf;
import math
from visualization_msgs.msg import Marker;
from visualization_msgs.msg import MarkerArray;
from aut_exploration.msg import *;
from geometry_msgs.msg import *;
from nav_msgs.msg import *;
from actionlib_msgs.msg import *;
from move_base_msgs.msg import *;
from smach_ros import ServiceState;
from std_msgs.msg import Header;
from tf import TransformListener;
from rail_object_detector.msg import *;



markers=[];
detectiontime=-1;
victims=[];
markcounter=0;
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
def elemntryMove(x,y):
        sac = actionlib.SimpleActionClient("move_base", MoveBaseAction);
        goal = MoveBaseGoal();
        goal.target_pose.pose.position.x = float(x);
        goal.target_pose.pose.position.y = float(y);
        goal.target_pose.pose.orientation.w = 1.0;
        goal.target_pose.header.frame_id = robotnamespace + "/odom";
        goal.target_pose.header.stamp = rospy.Time.now();
        sac.wait_for_server();
        sac.send_goal(goal);
        sac.wait_for_result();
def victim_callback2(data):
    global markcounter;
    global current_victim_status;
    global victims;
    global detectiontime;
    if  rospy.get_time()-detectiontime > 20 :
       print "vitim ditedted baby #######"
       detectiontime=rospy.get_time();
       x=data.x;
       y=data.y;
       mark_location(x,y,markcounter);
       current_victim_status="victim_detected";
       markcounter+=1;
       rospy.loginfo("victim detected at %f in the position %f--%f",detectiontime,x,y);
    #if data.

def victim_callback(data):
    global markcounter;
    global current_victim_status;
    global victims;
    global detectiontime;
    if len(data.objects)>0 and rospy.get_time()-detectiontime> 10 :
        if data.objects[0].label=="Human" :
            detectiontime=rospy.get_time();
            x=Odom_data.pose.pose.position.x;
            y=Odom_data.pose.pose.position.y;
            rospy.loginfo("victim detected at %f in the position %f--%f",detectiontime,x,y);
    #if data.
     #  victims.insert(len(victims),Odom_data.pose.pose.position);
      # current_victim_status="victim_detected";


def mark_location(x, y, mark_id):
    global markers;
    shape = Marker.CUBE;
    pub = rospy.Publisher('visualization_marker', MarkerArray, queue_size=100)

    for i in range(0,len(markers)):
        if in_range(x,y,markers[i].pose.position.x,markers[i].pose.position.y) < 4 :
            return;




    marker = Marker()
    marker.header.frame_id = "/map"
    marker.header.stamp = rospy.Time.now()


    marker.ns = "basic_shapes"
    marker.id = mark_id


    marker.type = shape


    marker.action = Marker.ADD


    marker.pose.position.x = x
    marker.pose.position.y = y
    marker.pose.position.z = 0
    marker.pose.orientation.x = 0.0
    marker.pose.orientation.y = 0.0
    marker.pose.orientation.z = 0.0
    marker.pose.orientation.w = 1.0


    marker.scale.x = 0.5
    marker.scale.y = 0.5
    marker.scale.z = 0.5


    marker.color.r = 0.0
    marker.color.g = 1.0
    marker.color.b = 0.0
    marker.color.a = 1.0

    marker.lifetime = rospy.Duration()
    markers.insert(len(markers),marker);

    rospy.loginfo(marker);
    pub.publish(markers);

    #rate.sleep()
    #while not rospy.is_shutdown():
    #    pub.publish(marker)
    #    rate.sleep()


def cancel_publisher():
    global move_base_cancel;
    move_base_cancel=rospy.Publisher("move_base/cancel",GoalID,10);


def in_range(x, y, w, z):
    return math.sqrt((x - w) ** 2 + (y - z) ** 2);


def setOdom(rawodomdata):
    global Odom_data;
    Odom_data = rawodomdata;

def setMap(costmap_data):
    global GCostmap_data;
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
    global current_goal_status;
    if len(data.status_list)==0 :
        return;
    current_goal_status = data.status_list[len(data.status_list) - 2].status;

# subscriber method from /move_base/status
def listener_goal_status():
    print "reading data";
    rospy.Subscriber("move_base/status", GoalStatusArray, callback_goal_status);
    rospy.Subscriber("odom", Odometry, setOdom);
    rospy.Subscriber("move_base/global_costmap/costmap", OccupancyGrid, setMap);
    rospy.Subscriber("victim_detected",Point,victim_callback2);



def Block_chosser(mapdata):
    global current_goal_status;
    # listener_goal_status()

    length = int(math.sqrt(len(mapdata)));
    dividor3 = int(length / 3);
    blocks = [];
    a = 0;
    for i in range(0, length, dividor3):
        for k in range(0, length, dividor3):
            blocks.insert(a,[]) ;
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
        return [-1, blocks[minIndex]];
    else:
        return [minIndex, blocks[minIndex]];




class myPoint():
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
        global GCostmap_data;
        global Odom_data;
        local_variable =GCostmap_data;
        rospy.loginfo("calculationg");
        # our code
        # goes in this
        # commented lines and points are created
        #
        lenght = local_variable.info.width ;
        x = (Odom_data.pose.pose.position.x - local_variable.info.origin.position.x) * 10;
        y = (Odom_data.pose.pose.position.y - local_variable.info.origin.position.y) * 10;
        lenght2 = local_variable.info.height ;
        if x < 275:
            x_gc = 0;
        elif x > lenght - 275:
            x_gc = int(lenght - 275);
        else:
            x_gc = int(x) - 270;
        if y < 275:
            y_gc = 0;
        elif y > lenght2 - 275:
            y_gc = int(lenght2 - 275);
        else:
            y_gc = int(y) - 270;

        Cell = [];
        for i in range(0, 180):
            Cell.extend(local_variable.data[(y_gc + i) * lenght:(1 + y_gc + i) * lenght]);
            if i == 90 :
                print "oh yeh";
                print (y_gc + i) * lenght;
                print len(local_variable.data);
        if len(Cell)<3 :
            print "oh yeh";
            print local_variable.info.width;
            print local_variable.info.height;
            print y_gc;
        resaultList = Block_chosser(Cell);
        block_index=resaultList[0];
        if block_index == -1:
            return "conntact the master";
        else:
            cx = x_gc / 10.0 + (block_index % 3) * 18.0 + 9.0;
            cy = y_gc / 10.0 + (int(block_index / 3)) * 18.0 + 9.0;
            self.center = myPoint(cx, cy);
            self.topLeft = myPoint(cx - 7, cy + 7);
            self.topRight = myPoint(cx + 7, cy + 7);
            self.bottomRight = myPoint(cx + 7, cy - 7);
            self.bottomLeft = myPoint(cx - 7, cy - 7);
            self.block = Block(self.center, self.topLeft, self.topRight, self.bottomRight, self.bottomLeft,
                               resaultList[1]);

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
        self.pointNumber=0;

    def odomCallback(data):
        pass;

    def move_to_goal(self, pos_x, pos_y, pos_z=0, ornt_w=1, ornt_x=0, ornt_y=0, ornt_z=1):
        # Simple Action Client
        global current_goal_status;
        global current_victim_status;
        sac = actionlib.SimpleActionClient("move_base", MoveBaseAction);
        print "aklsaklsdfjklsdjf3333333333333";

        # create goal
        goal = MoveBaseGoal();

        # set goal
        goal.target_pose.pose.position.x = pos_x;
        goal.target_pose.pose.position.y = pos_y;
        goal.target_pose.pose.orientation.w = ornt_w;
        goal.target_pose.pose.orientation.z = ornt_z;
        goal.target_pose.header.frame_id = robotnamespace + "/odom";
        goal.target_pose.header.stamp = rospy.Time.now();

        # start listener
        sac.wait_for_server();

        # send goal
        sac.send_goal(goal);
        odom_temp = Odom_data;
        rate = rospy.Rate(3);  # 10hz
        i = 0;
        while not rospy.is_shutdown():
            i+=1;
            if odom_temp.pose.pose.position.x == Odom_data.pose.pose.position.x and odom_temp.pose.pose.position.y == Odom_data.pose.pose.position.y:
                i += 1;
            else:
                odom_temp = Odom_data;
            if current_victim_status=="victim_detected" :
                a = rospy.Publisher("move_base/cancel", GoalID, queue_size=10);
                a.publish(GoalID());
                print "goal cancel shode aziam";
                rospy.sleep(15.0);
                current_victim_status="no victim";
                goal.target_pose.header.stamp = rospy.Time.now();
                sac.send_goal(goal);
            elif current_goal_status==3 or current_goal_status==4 or current_goal_status==5 or current_goal_status==9:
               rospy.sleep(0.4);
               if current_goal_status==3 or current_goal_status==4 or current_goal_status==5 or current_goal_status==9:
                  current_goal_status=43;
                  px=PxCalculator(self.block.matrix);
                  if px >75 :
                      self.status="fully explored";
                      print "fully explored move base finished";
                      return;
                  else:
                      self.status="not explored yet";
                      print "not explored yet move base finished";
                      return ;
            elif i==900 :
                i=0;
                px = PxCalculator(self.block.matrix);
                if px > 75:
                    self.status = "fully explored";
                    print "fully explored timed out";
                    return;
                else:
                    self.status = "not explored yet";
                    print "not explored yet timed out";
                    return;

            rate.sleep();


            # finish

            # print result
            # goal_result = sac.get_result()

    def execute(self, userdata):
        rospy.loginfo("Executing state Explore_Center");
        print self.count
        print "this was the number that you expected"
        a = userdata.EB_input;
        userdata.EB_output=a;
        if a.type == "Block" and self.count == 0:
            print "going to the center of the block";
            self.block = a;
            self.points = [ (a.center),(a.topLeft),(a.topRight),(a.bottomRight),(a.bottomLeft)];
            self.move_to_goal(self.points[self.count].x,self.points[self.count].y);
            if self.status=="not explored yet" :
                self.count+=1;
        elif a.type == "Block" and self.count > 0:
            print "going for the points";
            self.move_to_goal(self.points[self.count].x,self.points[self.count].y);
            if self.status=="not explored yet" :
                self.count+=1;
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
        self.goal=myPoint(data.pose.pose.position.x,data.pose.pose.position.y);
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
                i+=1;
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
    # Create the top level SMACH state machine
    listener_goal_status();
    rospy.sleep(2);

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
    rospy.init_node('smach_example_state_machine');
    robotnamespace = rospy.get_param("namespace");
    main();
    rospy.spin();
