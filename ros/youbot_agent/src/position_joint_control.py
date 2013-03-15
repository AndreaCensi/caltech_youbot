#!/usr/bin/env python

import roslib; roslib.load_manifest('youbot_agent')

import rospy #@UnresolvedImport
import brics_actuator.msg #@UnresolvedImport
import sys
import numpy as np
from velocity_joint_control import get_joint_velocity_msg
import pdb
import array_msgs.msg #@UnresolvedImport

def main(args):
    node_name = 'youbot_arm_position_controller'
    rospy.init_node(node_name)
    print('Node started')
    velocity_publisher = rospy.Publisher('/arm_1/arm_controller/velocity_command', brics_actuator.msg.JointVelocities)
    position_publisher = rospy.Publisher('/arm_1/arm_controller/position_command', brics_actuator.msg.JointPositions)

    def position_array_callback(msg):
        print('callback')
        print('Received array ' + str(msg.data))
        msg = get_joint_position_msg(msg.data, rospy.get_rostime())
        position_publisher.publish(msg)
    
    rospy.Subscriber('/youbot_arm/position_instruction', array_msgs.msg.FloatArray, position_array_callback)
    
    def stop_manipulator():
        print('Sending stop signal (zero velocity) to robot arm')
        # Finally stop the robot
        msg = get_joint_velocity_msg(np.zeros(5), rospy.get_rostime())
        velocity_publisher.publish(msg)
        
    rospy.on_shutdown(stop_manipulator)
#    rospy.spin()
    while not rospy.is_shutdown():
        try:
            sys.stdout.write('\033[45m' + node_name + '$\033[0m ')
            evaled = eval(sys.stdin.readline())
#            pdb.set_trace()
            if evaled.__class__ in [tuple, list]:
#                print('\033[91mError: Command not supported\033[0m')
                array = np.array(evaled)
                msg = get_joint_position_msg(array, rospy.get_rostime())
                position_publisher.publish(msg)
                print('Published position command: ' + str(array))
            else:
                print('\033[91mError: Unexpected command\033[0m')
                stop_manipulator()
        except:
            print('\033[91mError: Unexpected error occurred \033[0m')
            stop_manipulator()
#            pdb.set_trace()
    
    
def get_joint_position_msg(array, timeStamp=None):
    '''
    
    :param array:    float array with values to the joints
    '''
    
    num_joints = len(array)
    
    msg = brics_actuator.msg.JointPositions()
    msg.poisonStamp.description = 'Joint velocities generated with python by youbot_agent position_joint_control.'
    
    for i in range(num_joints):
        joint_value = brics_actuator.msg.JointValue()
        
        joint_value.joint_uri = 'arm_joint_' + str(i + 1)
        if timeStamp is not None:
            joint_value.timeStamp = timeStamp
        joint_value.unit = 'rad'
        joint_value.value = array[i]
        
        msg.positions.append(joint_value)
        
    assert len(msg.positions) == num_joints
    return msg

if __name__ == '__main__':
    main(sys.argv)
