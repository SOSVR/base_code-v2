#!/usr/bin/env python


# this file is a behavoir that we have created to to run a robot in full autonomous mode
# to do that we are using a stat machine created using the smach class of python
# using the smach is the main reasen we are using the python
# the robot will try to explore the it's global costmap by picking a 36 by 36 meter square and then it divides it into
# 9 smaller 18 by 18 meter blockes ...the robot it self is in the center block
# meaning the block with index of 4
# then the robot will calculate which one these blocks is explored less and the chossen block must be under 75 % explored
# after picking a cell the robot will try to visit the center and corners of the cell during this process the cell will be most probobly explored by more than 75 %
# so after that the robot will try to chose another cell and get explore it
# if by any chance all the 9 cells within the block are explored more than 75% then it will contact the master and try to get to somewhere that has no been explored yet
# when robot is moving if the robot detects a victim then the robot will enter the a state called victim detected and there
# inside that state it will wait for several seconds and then move
# however if before coming to this state robot will check to see if it has already seen the victim and then after that it will move on
import roslib;
import rospy;
import smach;
import smach_ros;
import actionlib;
import tf;
import math;
from visualization_msgs.msg import Marker;
from visualization_msgs.msg import MarkerArray;
from aut_exploration.msg import *;
from aut_exploration.srv import *;
from geometry_msgs.msg import *;
from nav_msgs.msg import *;
from actionlib_msgs.msg import *;
from move_base_msgs.msg import *;
from smach_ros import ServiceState;
from std_msgs.msg import Header;
from tf import TransformListener;
#from rail_object_detector.msg import *;



markers=[];
detection_time=-1;
victims=[];
mark_counter=0;
move_base_cancel_publisher=None;
GCostmap_data = None;
robot_name_space = None;
Odom_data = None;
current_victim_status=None;
current_goal_status = 0 ; # goal status--- PENDING=0--- ACTIVE=1---PREEMPTED=2--SUCCEEDED=3--ABORTED=4---REJECTED=5--PREEMPTING=6---RECALLING=7---RECALLED=8---LOST=9
sac=None;



def elemntry_move(x,y):
        global sac;
        goal = MoveBaseGoal();
        goal.target_pose.pose.position.x = float(x);
        goal.target_pose.pose.position.y = float(y);
        goal.target_pose.pose.orientation.w = 1.0;
        goal.target_pose.header.frame_id = robot_name_space + "/odom";
        goal.target_pose.header.stamp = rospy.Time.now();
        sac.send_goal(goal);
        sac.wait_for_result();


def victim_callback2(data):
    global mark_counter;
    global current_victim_status;
    global victims;
    global detection_time;
    if  rospy.get_time()-detection_time > 24 :
       x=data.x;
       y=data.y;
       print ("possible victim detected at x={} and y={}".format(x,y));
       detection_time=rospy.get_time();
       conform=mark_location(x,y,mark_counter);
       if conform == "invalid":
           return;
       current_victim_status="victim_detected";
       mark_counter+=1;
       rospy.loginfo("victim detected at %f in the position %f--%f",detection_time,x,y);

def victim_callback(data):
    global mark_counter;
    global current_victim_status;
    global victims;
    global detection_time;
    if len(data.objects)>0 and rospy.get_time()-detection_time> 10 :
        if data.objects[0].label=="Human" :
            detection_time=rospy.get_time();
            x=Odom_data.pose.pose.position.x;
            y=Odom_data.pose.pose.position.y;
            rospy.loginfo("victim detected at %f in the position %f--%f",detection_time,x,y);

    #if data.
     #  victims.insert(len(victims),Odom_data.pose.pose.position);
      # current_victim_status="victim_detected";


def mark_location(x, y, mark_id):
    #when we call this method , it checks the  array of existing markeres with the new marker
    #and if the new marker is not within 4 meters of any of the existing markers 
    #the new marker will be added to the arrey and it  will be shown on the rviz
    global markers;
    shape = Marker.CUBE;
    pub = rospy.Publisher('visualization_marker', MarkerArray, queue_size=100)

    for i in markers:
        if in_range(x,y,i.pose.position.x,i.pose.position.y) < 4 :
            return "invalid";


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
    return "valid";

    #rate.sleep()
    #while not rospy.is_shutdown():
    #    pub.publish(marker)
    #    rate.sleep()


def move_base_tools():
    global move_base_cancel_publisher;
    global sac;
    move_base_cancel_publisher=rospy.Publisher("move_base/cancel",GoalID,queue_size=10);
    sac = actionlib.SimpleActionClient("move_base", MoveBaseAction);
    sac.wait_for_server();



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
def start_listening():
    print ("reading data");
    rospy.Subscriber("move_base/status", GoalStatusArray, callback_goal_status);
    rospy.Subscriber("odom", Odometry, setOdom);
    rospy.Subscriber("move_base/global_costmap/costmap", OccupancyGrid, setMap);
    rospy.Subscriber("victim_detected",Point,victim_callback2);



def Block_chooser(mapdata):
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




class MyPoint():
    def __init__(self, xVector, yVector,inital_resault=None):
        self.type = "Point";
        self.resault = inital_resault;
        self.x = xVector;
        self.y = yVector;



class Block():

    def __init__(self, center, tl, tr, br, bl, matrix=[]):
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

class ChoseBlock(smach.State):
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
        rospy.loginfo("ChoseBlock Calculations");

        lenght = local_variable.info.width ;
        lenght2 = local_variable.info.height ;
        x = (Odom_data.pose.pose.position.x - local_variable.info.origin.position.x) * 10;
        y = (Odom_data.pose.pose.position.y - local_variable.info.origin.position.y) * 10;
        #we get the x and y of starting cell of the nine blocks as a whole
        # sincd  pose and origin positions are in meters we have to multiply by 10 since we have 10 cells per a meter (resulotion of cost map 0.1)
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
            #here we pick only the cells from the array of costmap that they fall inside the nine blocks
            # and because the array of costmap is in 1 deminsion i cant say data[i][j] instead i have to as follows
            Cell.extend(local_variable.data[(y_gc + i) * lenght:(1 + y_gc + i) * lenght]);
            if i == 90 :
                # it is for debugging
                print ("oh yeh");
                print ((y_gc + i) * lenght);
                print (len(local_variable.data));
        if len(Cell)<3 :
            #this if is for debugging and if the array named Cell has a lenght of smaller than 3 it tells us
            print ("oh yeh");
            print (local_variable.info.width);
            print (local_variable.info.height);
            print (y_gc);
        resaultList = Block_chooser(Cell);
        block_index=resaultList[0];
        if block_index == -1:
            return "conntact the master";
        else:
            #each block is 18 meter wide and long and x_gc and y_gc are the number of cells to the bottomLeft corner
            #of block so we have to divide it by 10 because 1 meter means 10 cells with a resulotion of 0.1
            cx = x_gc / 10.0 + (block_index % 3) * 18.0 + 9.0;
            cy = y_gc / 10.0 + (int(block_index / 3)) * 18.0 + 9.0;
            self.center = MyPoint(cx, cy);
            self.topLeft = MyPoint(cx - 7, cy + 7);
            self.topRight = MyPoint(cx + 7, cy + 7);
            self.bottomRight = MyPoint(cx + 7, cy - 7);
            self.bottomLeft = MyPoint(cx - 7, cy - 7);
            self.block = Block(self.center, self.topLeft, self.topRight, self.bottomRight, self.bottomLeft,
                               resaultList[1]);

    def execute(self, userdata):
        rospy.loginfo("Executing state Chose_block");
        a = self.Calculations();
        if a == "conntact the master":
            userdata.CB_output=MyPoint(Odom_data.x,Odom_data.y,"request_goal");
            return "no_block_found";
        else:
            userdata.CB_output = self.block;
            return "block_choosed";


# define state Explore_Center
##############################3
##############################
class ExploreBlock(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=["stucked", "exploration_completed", "exploration_failed", "point_reached","victim detected"],
                             input_keys=["EB_input"], output_keys=["EB_output"]);
        self.block = None;
        self.status = None;
        self.points = None;
        self.count = 0;
        self.pointNumber=0;


    def move_to_goal(self, pos_x, pos_y, pos_z=0, ornt_w=1, ornt_x=0, ornt_y=0, ornt_z=1):
        rospy.loginfo("sending goal inorder to explore a block");
        # Simple Action Client
        global current_goal_status;
        global current_victim_status;
        global sac;

        # create goal
        goal = MoveBaseGoal();

        # set goal
        goal.target_pose.pose.position.x = pos_x;
        goal.target_pose.pose.position.y = pos_y;
        goal.target_pose.pose.orientation.w = ornt_w;
        goal.target_pose.pose.orientation.z = ornt_z;
        goal.target_pose.header.frame_id = robot_name_space + "/odom";
        goal.target_pose.header.stamp = rospy.Time.now();

        # start listener

        # send goal
        sac.send_goal(goal);
        odom_temp = Odom_data;
        rate = rospy.Rate(3);  # 3hz
        i = 0;
        while not rospy.is_shutdown():
            i+=1;
            if odom_temp.pose.pose.position.x == Odom_data.pose.pose.position.x and odom_temp.pose.pose.position.y == Odom_data.pose.pose.position.y:
                i += 3;
            else:
                odom_temp = Odom_data;
            if current_victim_status=="victim_detected" :
                self.status="victim detected";
                rospy.loginfo("victim detected during exploration of a block");
                return;
            elif current_goal_status==3 or current_goal_status==4 or current_goal_status==5 or current_goal_status==9:
               rospy.sleep(0.4);
               if current_goal_status==3 or current_goal_status==4 or current_goal_status==5 or current_goal_status==9:
                  current_goal_status=43;
                  px=PxCalculator(self.block.matrix);
                  if px >75 :
                      self.status="fully explored";
                      print ("fully explored move base finished");
                      return;
                  else:
                      self.status="not explored yet";
                      print ("not explored yet move base finished");
                      return ;
            elif i>450 :
                i=0;
                px = PxCalculator(self.block.matrix);
                if px > 75:
                    self.status = "fully explored";
                    print ("fully explored timed out");
                    return;
                else:
                    self.status = "not explored yet";
                    print ("not explored yet timed out");
                    return;

            rate.sleep();


            # finish

            # print (result)
            # goal_result = sac.get_result()

    def execute(self, userdata):
        self.status=None;
        rospy.loginfo("Executing state ExploreBlock");
        print (self.count);
        print ("this was the number that you expected");
        a = userdata.EB_input;
        userdata.EB_output=a;
        if a.type == "Block" and self.count == 0:
            print ("going to the center of the block");
            self.block = a;
            self.points = [ (a.center),(a.topLeft),(a.topRight),(a.bottomRight),(a.bottomLeft)];
            self.move_to_goal(self.points[self.count].x,self.points[self.count].y);
            if self.status=="not explored yet" :
                self.count+=1;
        elif a.type == "Block" and self.count > 0:
            print ("going for the points");
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
        elif self.statu=="victim detected":
            return "victim detected";
        else:
            return "exploration_completed";


# define state Conntact_master
##############################
##############################


class ConntactMaster(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=["goal_received", "NOT_received", "map_fully_explored"],
                             input_keys=["CM_input"], output_keys=["CM_output"]);
        self.goal = None;
    def request_goal(self,current_pose):
        rospy.wait_for_service("request_fargoal")
        try:
            goal_request_service = rospy.ServiceProxy("request_fargoal", FarGoal);
            request=FarGoalRequest();
            request.pose_x=current_pose.x;
            request.pose_y=current_pose.y;
            request.request_type="goal";
            resp1 = goal_request_service(request);
            if(resp1.response_type=="yourgoal"):
                self.goal=MyPoint(resp1.goal_x,resp1.goal_y);
                return "goal_received";
            elif(resp1.response_type=="map_fully_explored"):
                return "map_fully_explored";
        except rospy.ServiceException, e:
            return "NOT_received";


    def request_different_goal(self,current_goal):
        rospy.wait_for_service("request_fargoal")
        try:
            goal_request_service = rospy.ServiceProxy("request_fargoal", FarGoal);
            request=FarGoalRequest();
            request.pose_x=current_goal.x;
            request.pose_y=current_goal.y;
            request.request_type="new_goal";
            resp1 = goal_request_service(request);
            if(resp1.response_type=="yourgoal"):
                self.goal=MyPoint(resp1.goal_x,resp1.goal_y);
                return "goal_received";
            elif(resp1.response_type=="map_fully_explored"):
                return "map_fully_explored";
        except rospy.ServiceException, e:
            return "NOT_received";




    def execute(self, userdata):
        rospy.loginfo("Executing state Conntact_master");
        a = "taher";
        if(userdata.CM_input.type=="Point"):
            if userdata.CM_input.resault=="request_goal":
                a=self.request_goal(userdata.CM_input);
            elif userdata.CM_input.resault=="stucked":
                a=self.request_different_goal(userdata.CM_input);
        if a == "goal received":
            userdata.CM_output=self.goal;
            return "goal_received";
        elif a == "map_fully_explored":
            return "map_fully_explored";
        else:
            userdata.CM_output=userdata.CM_input;
            return "NOT_received";


##############################
##############################


class GotoGoal(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=["goal_reached", "stucked", "failed_toMOVE","victim detected"], input_keys=["GG_input"], output_keys=["GG_output"]);
        self.goal = None;
        self.status=None;

    def move_to_goal(self,goal_x,goal_y, goal_z=0, ornt_w=1, ornt_x=0, ornt_y=0, ornt_z=1):
        rospy.loginfo("sending goal inorder to go to a very far goal");
        global sac;
        global current_goal_status;
        global current_victim_status;
        # create goal
        self.goal=MyPoint(goal_x,goal_y);
        fargoal = MoveBaseGoal();
        # set goal
        fargoal.target_pose.pose.position.x = goal_x;
        fargoal.target_pose.pose.position.y = goal_y;
        fargoal.target_pose.pose.orientation.w = ornt_w;
        fargoal.target_pose.pose.orientation.z = ornt_z;
        fargoal.target_pose.header.frame_id = robot_name_space + "/odom";
        fargoal.target_pose.header.stamp = rospy.Time.now();
        # send goal
        sac.send_goal(fargoal);
        odom_temp = Odom_data;
        rate = rospy.Rate(3);  # 3hz
        i = 0;
        j = 0;
        while not rospy.is_shutdown():
            i+=1;
            if odom_temp.pose.pose.position.x == Odom_data.pose.pose.position.x and odom_temp.pose.pose.position.y == Odom_data.pose.pose.position.y:
                i += 2;
                j += 1;
            else:
                odom_temp = Odom_data;
            if current_victim_status=="victim_detected" :
                self.status="victim detected";
                rospy.loginfo("victim detected when moving to a very far goal");
                return;
            elif current_goal_status==3 or current_goal_status==4 or current_goal_status==5 or current_goal_status==9:
               rospy.sleep(0.4);
               if (current_goal_status==3 ):
                  self.status="goal_reached";
                  current_goal_status=43;
                  return;
               elif (current_goal_status==4 or current_goal_status==5 or current_goal_status==9 ):
                  current_goal_status=43;
                  self.status="stucked";
                  self.goal.resault="stucked";
                  return;

            elif i==450 :
                i=0;
                j=0;
                self.status="stucked";
                self.goal.resault="stucked";
                return;
            elif j > 100 :
                i=0;
                j=0;
                self.state="failed_toMOVE";
                return;

            rate.sleep();


            # finish

            # print (result)
            # goal_result = sac.get_result()


    def execute(self, userdata):
        self.status=None;
        rospy.loginfo("Executing state GOTO_Goal");
        if (userdata.GG_input.type=="Point"):
            move_to_goal(userdata.GG_input.x,userdata.GG_input.x);
        userdata.GG_output=self.goal;
        if self.status=="goal_reached":
            return "goal_reached";
        elif self.status=="stucked":
            return "stucked";
        elif self.status=="victim detected":
            return "victim detected" ;
        elif self.status=="failed_toMOVE":
            return "failed_toMOVE";




# define the state VictimDetected
##############################
##############################


class VictimDetected(smach.State):

    def __init__(self):
        smach.State.__init__(self, outcomes=["keep exploring", "go to goal"], input_keys=["VD_input"],output_keys=["VD_output"]);
        self.goal = None;

    def waiting(self):
        global move_base_cancel_publisher;
        move_base_cancel_publisher.publish(GoalID());
        print ("goal was canceled due to the detected vitcim");
        rospy.sleep(10.0);
        current_victim_status="no victim";


    def execute(self, userdata):
        rospy.loginfo("Executing state VictimDetected");
        self.waiting();
        userdata.VD_output=userdata.VD_input;
        if userdata.VD_input.type == "Block":
            return "keep exploring";
        else:
            return "go to goal";






# define the states of the nested state machine called recovery
##############################
##############################



class SimpleState(smach.State):
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
    start_listening();
    move_base_tools();
    rospy.sleep(2);

    sm_exploration = smach.StateMachine(outcomes=["hold", "shut_down"]);

    # Open the container
    with sm_exploration:
        smach.StateMachine.add("Chose_block", ChoseBlock(),
                               transitions={"block_choosed": "Explore_Block", "no_block_found": "Conntact_master"},
                               remapping={"CB_input": "passing_data", "CB_output": "passing_data"});


        smach.StateMachine.add("Explore_Block", ExploreBlock(),
                               transitions={"point_reached": "Explore_Block", "exploration_failed": "recovery",
                                            "exploration_completed": "Chose_block", "stucked": "Chose_block","victim detected":"Victim_Detected"},
                               remapping={"EB_input": "passing_data", "EB_output": "passing_data"});


        smach.StateMachine.add("Conntact_master", ConntactMaster(),
                               transitions={"map_fully_explored": "hold", "goal_received": "GOTO_Goal",
                                            "NOT_received": "Conntact_master"},
                               remapping={"CM_input": "passing_data", "CM_output": "passing_data"});


        smach.StateMachine.add("GOTO_Goal", GotoGoal(),
                               transitions={"goal_reached": "Chose_block", "stucked": "Conntact_master",
                                            "failed_toMOVE": "recovery","victim detected":"Victim_Detected"},
                               remapping={"GG_input": "passing_data", "GG_output": "passing_data"});

        smach.StateMachine.add("Victim_Detected", VictimDetected(),
                               transitions={"go to goal": "GOTO_Goal", "keep exploring": "Explore_Block"},
                               remapping={"VD_input": "passing_data", "VD_output": "passing_data"});


        # Create the sub SMACH state machine
        sm_recovery = smach.StateMachine(outcomes=["recovery_completed", "recovery_failed"]);

        # Open the container
        with sm_recovery:
            # Add states to the container

            smach.StateMachine.add("simple_state", SimpleState(),
                                   transitions={"shuting_down": "recovery_failed", "comon": "recovery_completed"});

        smach.StateMachine.add("recovery", sm_recovery,
                               transitions={"recovery_failed": "shut_down", "recovery_completed": "Chose_block"});

        # Execute SMACH plan
    aut_explore = sm_exploration.execute();


if __name__ == '__main__':
    rospy.init_node('smach_example_state_machine');
    robot_name_space = rospy.get_param("namespace", default="sos1");
    main();
    rospy.spin();
