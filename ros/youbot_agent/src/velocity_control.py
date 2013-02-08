#!/usr/bin/env python
import roslib; roslib.load_manifest('youbot_agent')

import rospy #@UnresolvedImport
import brics_actuator.msg #@UnresolvedImport
import sys
import numpy as np
import array_msgs.msg #@UnresolvedImport
import geometry_msgs.msg #@UnresolvedImport
import pdb
from velocity_base_control import get_twist_velocity_msg
from velocity_joint_control import get_joint_velocity_msg

def main(args):
    node_name = 'youbot_velocity_control'
    rospy.init_node(node_name)
    print('Node started')
    base_publisher = rospy.Publisher('/cmd_vel', geometry_msgs.msg.Twist)
    arm1_publisher = rospy.Publisher('/arm_1/arm_controller/velocity_command', brics_actuator.msg.JointVelocities)
    
    def velocity_array_callback(msg):
        print('Received array ' + str(msg.data))
        base_msg = get_twist_velocity_msg(msg.data[:3], rospy.get_rostime())
        arm_msg = get_joint_velocity_msg(msg.data[3:], rospy.get_rostime())
        base_publisher.publish(base_msg)
        arm1_publisher.publish(arm_msg)
#        msg = get_joint_velocity_msg(msg.data, rospy.get_rostime())
#        velocity_publisher.publish(msg)
    
    rospy.Subscriber('/youbot/velocity_instruction', array_msgs.msg.FloatArray, velocity_array_callback)
    
    def stop_manipulator():
        print('Shutting down')
        # Finally stop the robot
        base_msg = get_twist_velocity_msg([0, 0, 0], rospy.get_rostime())
        arm_msg = get_joint_velocity_msg([0, 0, 0, 0, 0], rospy.get_rostime())
        base_publisher.publish(base_msg)
        arm1_publisher.publish(arm_msg)
        print('Signal stop sent')
        
    rospy.on_shutdown(stop_manipulator)
    while not rospy.is_shutdown():
        try:
            sys.stdout.write('\033[45m' + node_name + '$\033[0m ')
            evaled = eval(sys.stdin.readline())
            print(str(evaled))
#            pdb.set_trace()
            if evaled.__class__ in [tuple, list]:
#                print('\033[91mError: Command not supported\033[0m')
                array = np.array(evaled)
                base_msg = get_twist_velocity_msg(array[:3], rospy.get_rostime())
                arm_msg = get_joint_velocity_msg(array[3:], rospy.get_rostime())
                base_publisher.publish(base_msg)
                arm1_publisher.publish(arm_msg)
                print('Published velocity command: ' + str(array))
            else:
                print('\033[91mError: Unexpected command\033[0m')
                base_msg = get_twist_velocity_msg([0, 0, 0], rospy.get_rostime())
                arm_msg = get_joint_velocity_msg([0, 0, 0, 0, 0], rospy.get_rostime())
                base_publisher.publish(base_msg)
                arm1_publisher.publish(arm_msg)
        except:
            print('\033[91mError: Unexpected error occurred \033[0m')
            base_msg = get_twist_velocity_msg([0, 0, 0], rospy.get_rostime())
            arm_msg = get_joint_velocity_msg([0, 0, 0, 0, 0], rospy.get_rostime())
            base_publisher.publish(base_msg)
            arm1_publisher.publish(arm_msg)
    
if __name__ == '__main__':
    main(sys.argv)
