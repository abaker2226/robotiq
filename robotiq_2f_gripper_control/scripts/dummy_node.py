#!/usr/bin/env python3
import rospy
from std_msgs.msg import String

def main():
    rospy.init_node('dummy_node')
    pub = rospy.Publisher('/gripper_topic', String, queue_size=10)
    rospy.loginfo("DummyNode ready. Type 'left open', 'right close', etc. and press ENTER.")

    while not rospy.is_shutdown():
        cmd = input("Type command (left/right open/close): ").strip().lower()
        if cmd in ['left open', 'left close', 'right open', 'right close']:
            pub.publish(cmd)
            rospy.loginfo(f"Published: {cmd}")
        else:
            rospy.logwarn("Use: 'left open', 'left close', 'right open', or 'right close'.")

if __name__ == '__main__':
    main()
