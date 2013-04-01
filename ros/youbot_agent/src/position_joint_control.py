#!/usr/bin/env python

import roslib; roslib.load_manifest('youbot_agent')

import rospy #@UnresolvedImport
import brics_actuator.msg #@UnresolvedImport
import sys
import numpy as np

from velocity_joint_control import get_joint_velocity_msg

import array_msgs.msg #@UnresolvedImport

def main(args):
    node_name = 'youbot_arm_position_controller'
    rospy.init_node(node_name)
    rospy.loginfo('Arm position controller started.')
    velocity_publisher = rospy.Publisher('/arm_1/arm_controller/velocity_command', brics_actuator.msg.JointVelocities)
    position_publisher = rospy.Publisher('/arm_1/arm_controller/position_command', brics_actuator.msg.JointPositions)

    def position_array_callback(msg):
        rospy.loginfo('callback, received array %s' % msg)
        # print('callback')
        # print('Received array ' + str(msg.data))
        msg = get_joint_position_msg(msg.data, rospy.get_rostime())
        position_publisher.publish(msg)
    
    rospy.Subscriber('/youbot_arm/position_instruction', array_msgs.msg.FloatArray, position_array_callback)
    
    def stop_manipulator():
        rospy.logerr('Sending stop signal (zero velocity) to robot arm')
        msg = get_joint_velocity_msg(np.zeros(5), rospy.get_rostime())
        velocity_publisher.publish(msg)
        
    rospy.on_shutdown(stop_manipulator)

    while not rospy.is_shutdown():
        try:
            array = read_array(prompt=node_name)
            msg = get_joint_position_msg(array, rospy.get_rostime())
            position_publisher.publish(msg)    
            rospy.loginfo('Published position command: ' + str(array))

        except Exception as e:
            rospy.logerr('Unexpected error occurred (%s: %s).' % (type(e), e))
            print('\033[91mError: Unexpected error occurred \033[0m')
            stop_manipulator()

def read_array(prompt='>'):
    """ Reads a line and tries to evaluate it. Returns an array or Exception."""
    line = read_line(prompt=prompt)

    try:
        evaled = eval(line)
    except:
        raise Exception('Could not evaluate %r' % line)

    if evaled.__class__ in [tuple, list]:
        array = np.array(evaled)
        return array
    else:
        raise Exception('Not an array:' % line) 
    
def read_line(prompt='>'):
    """ Returns a string """
    sys.stdout.write('\033[45m' + prompt + '$\033[0m ')
    line = sys.stdin.readline()
    return line
    
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
