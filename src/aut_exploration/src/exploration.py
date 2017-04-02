#!/usr/bin/env python

import roslib;
import rospy;
import smach;
import smach_ros;
from aut_exploration.msg import *


class Point():
    def __init__(self,xVector,yVector):
        self.x=xVector;
        self.y=yVector;



class Block():
    def __init__(self,center,tl,tr,br,bl):
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


# define state Chose_block
##############################3
##############################

class Chose_block(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=["block_choosed","no_block_found"],output_keys=["CB_output"]);
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
        self.block=Block(self.center,self.topLeft,self.topRight,self.bottomRight,self.bottomLeft);

    def execute(self, userdata):
        rospy.loginfo("Executing state Chose_block");
        a="taher";
        if a=="javadi":
            return "block_choosed";
        else:
            return "no_block_found";

# define state Explore_Center
##############################3
##############################
class Explore_Center(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=["stucked","exploration_completed","exploration_failed","center_reached"],input_keys=["EC_input"],output_keys=["EC_output"]);
        self.block=None;
        self.center=None;
        self.topLeft=None;
        self.topRight=None;
        self.bottomRight=None;
        self.bottomLeft=None;

    def Calculations():
        rospy.loginfo("calculationg");

    def execute(self, userdata):
        rospy.loginfo("Executing state Explore_Center");
        a="javadi";
        if a=="taher":
            return "stucked";
        elif a=="gohari":
            return "exploration_failed";
        elif a=="azami":
            return "center_reached";
        else:
            return "exploration_completed";



# define state Explore_Next_corner
##############################3
##############################
class Explore_Next_corner(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=["stucked","exploration_completed","exploration_failed","corner_reached","all_corners_visited"],input_keys=["ENC_input"],output_keys=["ENC_output"]);
        self.counter=0;
        self.block=None;
        self.center=None;
        self.topLeft=None;
        self.topRight=None;
        self.bottomRight=None;
        self.bottomLeft=None;

    def Calculations():
        rospy.loginfo("calculationg");

    def execute(self, userdata):
        rospy.loginfo("Executing state Explore_Next_corner");
        a="javadi";
        if a=="shiri":
            return "stucked";
        elif a=="gohari":
            return "exploration_failed";
        elif a=="azami":
            return "corner_reached";
        elif a=="taher":
            return "all_corners_visited";
        else:
            return "exploration_completed";

# define state Chose_different_block
##############################3
##############################

class Chose_different_block(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=["block_choosed","no_block_found"],input_keys=["CDB_input"],output_keys=["CDB_output"]);
        self.block=None;
        self.center=None;
        self.topLeft=None;
        self.topRight=None;
        self.bottomRight=None;
        self.bottomLeft=None;

    def Calculations():
        rospy.loginfo("calculationg");

    def execute(self, userdata):
        rospy.loginfo("Executing state Chose_different_block");
        a="taher";
        if a=="javadi":
            return "block_choosed";
        else:
            return "no_block_found";
# define state Conntact_master
##############################3
##############################


class Conntact_master(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=["goal_received","NOT_received","map_fully_explored"],output_keys=["CM_output"]);
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

class Request_different_goal(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=["goal_received","NOT_received","map_fully_explored"],input_keys=["RDG_input"],output_keys=["RDG_output"]);
        self.goal=None;

    def Calculations():
        rospy.loginfo("calculationg");

    def execute(self, userdata):
        rospy.loginfo("Executing state Request_different_goal");
        a="taher";
        if a=="javadi":
            return "goal_received";
        elif a=="azami":
            return "map_fully_explored";
        else:
            return "NOT_received";



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

def main():
    rospy.init_node('smach_example_state_machine')

    # Create the top level SMACH state machine
    sm_exploration = smach.StateMachine(outcomes=["hold","shut_down"])

    # Open the container
    with sm_exploration:
           smach.StateMachine.add("Chose_block",Chose_block(),transitions={"block_choosed":"Explore_Center","no_block_found":"Conntact_master"},remapping={"CB_output":"azami_data"});
           smach.StateMachine.add("Explore_Center",Explore_Center(),transitions={"center_reached":"Explore_Next_corner","exploration_failed":"recovery","exploration_completed":"Chose_block","stucked":"Chose_different_block"},remapping={"EC_input":"azami_data","EC_output":"gohari_data"});
           smach.StateMachine.add("Explore_Next_corner",Explore_Next_corner(),transitions={"exploration_failed":"recovery","all_corners_visited":"Chose_different_block","stucked":"Chose_different_block","exploration_completed":"Chose_block","corner_reached":"Explore_Next_corner"},remapping={"ENC_input":"gohari_data","ENC_output":"gohari_data"});
           smach.StateMachine.add("Chose_different_block",Chose_different_block(),transitions={"block_choosed":"Explore_Center","no_block_found":"Conntact_master"},remapping={"CDB_input":"gohari_data","CDB_output":"azami_data"});
           smach.StateMachine.add("Conntact_master",Conntact_master(),transitions={"map_fully_explored":"hold","goal_received":"GOTO_Goal","NOT_received":"Conntact_master"},remapping={"CM_output":"mamin_data"});
           smach.StateMachine.add("GOTO_Goal",GOTO_Goal(),transitions={"goal_reached":"Chose_block","stucked":"Request_different_goal","failed_toMOVE":"recovery"},remapping={"GG_input":"mamin_data","GG_output":"taher_data"});
           smach.StateMachine.add("Request_different_goal",Request_different_goal(),transitions={"goal_received":"GOTO_Goal","map_fully_explored":"hold","NOT_received":"Request_different_goal"},remapping={"RDG_input":"taher_data","RDG_output":"mamin_data"});





           # Create the sub SMACH state machine
           sm_recovery = smach.StateMachine(outcomes=["recovery_completed","recovery_failed"]);

           # Open the container
           with sm_recovery:

              # Add states to the container

              smach.StateMachine.add("simple_state", a_simple_state(), transitions={"shuting_down":"recovery_failed","comon":"recovery_completed"});





           smach.StateMachine.add("recovery", sm_recovery,transitions={"recovery_failed":"shut_down","recovery_completed":"Chose_block"});

           # Execute SMACH plan
    aut_explore = sm_exploration.execute();



if __name__ == '__main__':
    kiseh=Block_msgs();
    print kiseh.center_x;
