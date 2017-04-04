#!/usr/bin/env python

import roslib;
import rospy;
import smach;
import smach_ros;
import actionlib;
import tf;
import math
from aut_exploration.msg import * ;
from geometry_msgs.msg import * ;
from nav_msgs.msg import * ;
from actionlib_msgs.msg import * ;
from move_base_msgs.msg import * ;
from smach_ros import ServiceState ;
from std_msgs.msg import Header ;
from tf import TransformListener ;

class Point():
    def __init__(self,xVector,yVector):
        self.type="Point";
        self.resault=None;
        self.x=xVector;
        self.y=yVector;
    def get_Type(self):
        return self.type;



class Block():
    def __init__(self,center,tl,tr,br,bl):
        self.type="Block";
        self.center=center;
        self.topLeft=tl;
        self.topRight=tr;
        self.bottomRight=br;
        self.bottomLeft=bl;
    def get_Center(self):
        return self.center;
    def get_TL(self):
        return self.topLeft;
    def get_TR(self):
        return self.topRight;
    def get_BR(self):
        return self.bottomRight;
    def get_BL(self):
        return self.bottomLeft;
    def get_Type(self):
        return self.type;


# define state Chose_block
##############################3
##############################

class Chose_block(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=["block_choosed","no_block_found"],input_keys=["CB_input"],output_keys=["CB_output"]);
        self.counter = 0
        self.block=None;
        self.center=None;
        self.topLeft=None;
        self.topRight=None;
        self.bottomRight=None;
        self.bottomLeft=None;

    def Calculations():
        rospy.loginfo("calculationg");
        #our code
        #goes in this
        #commented lines and points are created
        #
        length=Costmap_data.info.width*10;
        x=(Odom_data.pose.pose.position.x-GCostmap_data.info.origin.position.x)*10;
        y=(Odom_data.pose.pose.position.y-GCostmap_data.info.origin.position.y)*10;



        if x<275 :
            x_gc=0;
        elif x>lenght- 275 :
            x_gc=int(lenght - 275);
        else :
            x_gc=int(x)-270;
        if y<275 :
            y_gc=0;
        elif y>lenght- 275 :
            y_gc=int(lenght - 275);
        else :
            y_gc=int(y)-270;

        Cell=[];
        for i in range(0,180) :
            Cell.extend(GCostmap_data.data[(y_gc+i)*length:(1+y_gc+i)*length]);
        block_index=Block_chosser(Cell);
        if block_index==-1 :
            return "conntact the master";
        else :
            cx=x_gc/10.0 +(block_index%3)*18.0+9.0;
            cy=y_gc/10.0 +(int(block_index/3))*18.0+9.0;
            self.center=Point(cx,cy);
            self.topLeft=Point(cx-7,cy+7);
            self.topRight=Point(cx+7,cy+7);
            self.bottomRight=Point(cx+7,cy-7);
            self.bottomLeft=Point(cx-7,cy-7);
            self.block=Block(self.center,self.topLeft,self.topRight,self.bottomRight,self.bottomLeft);

    def execute(self, userdata):
        rospy.loginfo("Executing state Chose_block");
        a=Calculations();
        if a=="conntact the master" :
            return "no_block_found";
        else :
            userdata.CB_output=self.block;
            return "block_choosed";



# define state Explore_Center
##############################3
##############################
class Explore_Block(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=["stucked","exploration_completed","exploration_failed","point_reached"],input_keys=["EB_input"],output_keys=["EB_output"]);
        self.block=None;
        self.status=None;
        self.points=None;
        self.count=0;

    def odomCallback(data):
        pass;

    def move_to_goal(goal):
        rospy.loginfo("calculationg");

    def execute(self, userdata):
        rospy.loginfo("Executing state Explore_Center");
        a=userdata.EB_input;
        if a.get_Type()=="Block" and self.count==0 :
            self.block=a;
            self.points=[];
            self.points[0]=a.get_Center();
            self.points[1]=a.get_TL();
            self.points[2]=a.get_TR();
            self.points[3]=a.get_BR();
            self.points[4]=a.get_BL();
            move_to_goal(self.points[0]);
        elif a.get_Type()=="Block" and self.count>0 :
            move_to_goal(self.points[self.count]);
            self.count+=1;
            if self.count > 4 :
                if self.status=="not explored yet" :
                    self.status="exploration failed";
                self.count=0;



        if self.status=="fully explored":
            return "exploration_completed";
        elif self.status=="exploration failed":
            return "exploration_failed";
        elif self.status=="not explored yet":
            return "point_reached";
        else:
            return "exploration_completed";



# define state Explore_Next_corner
##############################3
##############################

# define state Chose_different_block
##############################3
##############################


# define state Conntact_master
##############################3
##############################


class Conntact_master(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=["goal_received","NOT_received","map_fully_explored"],input_keys=["CM_input"],output_keys=["CM_output"]);
        self.goal=None;

    def Calculations():
        rospy.loginfo("calculationg");

    def execute(self, userdata):
        rospy.loginfo("Executing state Conntact_master");
        a="taher";
        if a=="javadi":
            return "goal_received";
        elif a=="azami":
            return "map_fully_explored";
        else:
            return "NOT_received";


##############################3
##############################



class GOTO_Goal(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=["goal_reached","stucked","failed_toMOVE"],input_keys=["GG_input"],output_keys=["GG_output"]);
        self.goal=None;

    def Calculations():
        rospy.loginfo("calculationg");

    def execute(self, userdata):
        rospy.loginfo("Executing state GOTO_Goal");
        a="taher";
        if a=="javadi":
            return "goal_reached";
        elif a=="azami":
            return "stucked";
        else:
            return "failed_toMOVE";


# define state Request_different_goal
##############################3
##############################



class a_simple_state(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=["shuting_down","comon"]);

    def Calculations():
        rospy.loginfo("calculationg");

    def execute(self, userdata):
        rospy.loginfo("Executing state Request_different_goal");
        a="taher";
        if a=="javadi":
            return "shuting_down";
        else:
            return "comon";





# our main function
##############################3
##############################
def Block_chosser(mapdata):
       length =int(math.sqrt(len(mapdata)));
       dividor3=int(length/3);
       blocks=[];
       a=0;
       for i in range(0,length,dividor3):
           for k in range(0,length,dividor3):
               blocks[a]=[];
               for j in range(0,dividor3):
                   blocks[a].extend(mapdata[i*length+j*length+k:i*length+j*length+k+dividor3-1]);
       a+=1;
       minPX=PxCalculator(blocks[0]);
       minIndex=0;
       for w in range(1,9):
           if PxCalculator(blocks[w])< minPX :
               minPX=PxCalculator(blocks[w]);
               minIndex=w;

       if minPX>75 :
            return -1;
       else:
            return minIndex;


def PxCalculator(mapdata):
    sum=0;
    for i in range(0,len(mapdata)):
         if mapdata[i]>=0 :
            sum+=1;
         else:
            sum-=1;
    final_sum =(sum+len(mapdata))/(2*len(mapdata))*100;
    return final_sum;



def main():
    rospy.init_node('smach_example_state_machine');

    Odom_topic="/%s/odom" %(robotnamespace);
    rospy.Subscriber(Odom_topic, Odometry, setOdom);
    global_costmap_topic="/%s/move_base/global_costmap/costmap" % (robotnamespace);
    rospy.Subscriber(global_costmap_topic,OccupancyGrid,setMap);



       # Create the top level SMACH state machine
    sm_exploration = smach.StateMachine(outcomes=["hold","shut_down"]);

    # Open the container
    with sm_exploration:
           smach.StateMachine.add("Chose_block",Chose_block(),transitions={"block_choosed":"Explore_Block","no_block_found":"Conntact_master"},remapping={"CB_input":"passing_data","CB_output":"passing_data"});
           smach.StateMachine.add("Explore_Block",Explore_Block(),transitions={"point_reached":"Explore_Block","exploration_failed":"recovery","exploration_completed":"Chose_block","stucked":"Chose_block"},remapping={"EB_input":"passing_data","EB_output":"passing_data"});
           smach.StateMachine.add("Conntact_master",Conntact_master(),transitions={"map_fully_explored":"hold","goal_received":"GOTO_Goal","NOT_received":"Conntact_master"},remapping={"CM_input":"passing_data","CM_output":"passing_data"});
           smach.StateMachine.add("GOTO_Goal",GOTO_Goal(),transitions={"goal_reached":"Chose_block","stucked":"Conntact_master","failed_toMOVE":"recovery"},remapping={"GG_input":"passing_data","GG_output":"passing_data"});





           # Create the sub SMACH state machine
           sm_recovery = smach.StateMachine(outcomes=["recovery_completed","recovery_failed"]);

           # Open the container
           with sm_recovery:

              # Add states to the container

              smach.StateMachine.add("simple_state", a_simple_state(), transitions={"shuting_down":"recovery_failed","comon":"recovery_completed"});





           smach.StateMachine.add("recovery", sm_recovery,transitions={"recovery_failed":"shut_down","recovery_completed":"Chose_block"});

           # Execute SMACH plan
    aut_explore = sm_exploration.execute();




def setOdom(rawodomdata):
    Odom_data=rawodomdata;

def setMap(costmap_data):
    GCostmap_data=costmap_data;


GCostmap_data=None;
robotnamespace=None;
Odom_data=None;

if __name__ == '__main__':
    robotnamespace=rospy.get_param("namespace");
    print
    main();
