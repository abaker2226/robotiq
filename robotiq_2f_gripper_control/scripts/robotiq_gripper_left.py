#!/usr/bin/env python3
import rospy
import actionlib
from std_msgs.msg import String
from robotiq_2f_gripper_msgs.msg import CommandRobotiqGripperAction, CommandRobotiqGripperGoal

HOLD_POSITION = 0.0
OPEN_POSITION = 0.140
FORCE = 15.0

class GripperCmdNode:
    def __init__(self):
        self.client = actionlib.SimpleActionClient('/left_gripper/command_robotiq_action', CommandRobotiqGripperAction)
        rospy.loginfo("[left_gripper] Waiting for action server...")
        self.client.wait_for_server()
        rospy.loginfo("[left_gripper] Connected to action server.")
        self.current_state = None
        rospy.Subscriber("/gripper_topic", String, self.cmd_cb)

    def cmd_cb(self, msg):
        tokens = msg.data.lower().split()
        if len(tokens) != 2:
            return
        gripper, cmd = tokens
        if gripper != "left":
            return
        if cmd == self.current_state:
            return
        if cmd == "open":
            self.send_goal(OPEN_POSITION)
            self.current_state = "open"
        elif cmd == "close":
            self.send_goal(HOLD_POSITION)
            self.current_state = "close"

    def send_goal(self, pos):
        goal = CommandRobotiqGripperGoal()
        goal.position = pos
        goal.speed = 0.05
        goal.force = FORCE
        goal.emergency_release = False
        goal.stop = False
        rospy.loginfo(f"[left_gripper] Sending goal: {pos}")
        self.client.send_goal_and_wait(goal)

if __name__ == "__main__":
    rospy.init_node("robotiq_gripper_left")
    GripperCmdNode()
    rospy.spin()
