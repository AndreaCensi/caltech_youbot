#!/usr/bin/env python
import roslib; roslib.load_manifest('youbot_agent')

import rospy #@UnresolvedImport
import brics_actuator.msg #@UnresolvedImport
import sys
import numpy as np
import array_msgs.msg #@UnresolvedImport
import pdb

def main(args):
    node_name = 'youbot_arm_incremental_control'
    rospy.init_node(node_name)
    print('Node started')
    velocity_publisher = rospy.Publisher('/arm_1/arm_controller/velocity_command', brics_actuator.msg.JointVelocities)
    delay = 0.2
    rate = 2
    def increment_array_callback(msg):
        print('Received array ' + str(msg.data))
        msg = get_joint_velocity_msg(msg.data, rospy.get_rostime())
        velocity_publisher.publish(msg)
        rospy.sleep(1./rate)
        msg = get_joint_velocity_msg([0, 0, 0, 0, 0, 0, 0], rospy.get_rostime())
        velocity_publisher.publish(msg)
        
    rospy.Subscriber('/youbot_arm/incremental_instruction', array_msgs.msg.FloatArray, increment_array_callback)
    
    def stop_manipulator():
        print('Shutting down')
        # Finally stop the robot
        msg = get_joint_velocity_msg(np.zeros(5), rospy.get_rostime())
        velocity_publisher.publish(msg)
        print('Signal stop sent')
        
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
                msg = array_msgs.msg.FloatArray()
                msg.data = array
#                msg = get_joint_velocity_msg(array, rospy.get_rostime())
                increment_array_callback(msg)
#                velocity_publisher.publish(msg)
                print('Published velocity command: ' + str(array))
            else:
                print('\033[91mError: Unexpected command\033[0m')
                
                msg = array_msgs.msg.FloatArray()
                msg.data = [0, 0, 0, 0, 0, 0, 0]
#                velocity_publisher.publish(msg)
#                msg = get_joint_velocity_msg([0, 0, 0, 0, 0, 0, 0], rospy.get_rostime())
                increment_array_callback(msg)
        except:
            print('\033[91mError: Unexpected error occurred \033[0m')
#            msg = get_joint_velocity_msg([0, 0, 0, 0, 0, 0, 0], rospy.get_rostime())
#            velocity_publisher.publish(msg)
            msg = array_msgs.msg.FloatArray()
            msg.data = [0, 0, 0, 0, 0, 0, 0]
            increment_array_callback(msg)
    

def get_joint_velocity_msg(array, timeStamp=None):
    '''
    
    :param array:    float array with values to the joints
    '''
    
    num_joints = len(array)
    
    msg = brics_actuator.msg.JointVelocities()
    msg.poisonStamp.description = 'Joint velocities generated with python by youbot_demo arm_velocity_demo.'
    
    for i in range(num_joints):
        joint_value = brics_actuator.msg.JointValue()
        
        joint_value.joint_uri = 'arm_joint_' + str(i + 1)
        if timeStamp is not None:
            joint_value.timeStamp = timeStamp
        joint_value.unit = 's^-1 rad'
        joint_value.value = array[i]
        
        msg.velocities.append(joint_value)
        
    assert len(msg.velocities) == num_joints
    return msg

if __name__ == '__main__':
    main(sys.argv)
