#!/usr/bin/env python
import roslib; roslib.load_manifest('youbot_agent')

import rospy #@UnresolvedImport
import brics_actuator.msg #@UnresolvedImport
import sys
import numpy as np
import array_msgs.msg #@UnresolvedImport
import geometry_msgs.msg #@UnresolvedImport
import pdb

def main(args):
    node_name = 'youbot_base_velocity_control'
    rospy.init_node(node_name)
    print('Node started')
    velocity_publisher = rospy.Publisher('/cmd_vel', geometry_msgs.msg.Twist)
    
    def velocity_array_callback(msg):
        print('Received array ' + str(msg.data))
        #msg = get_joint_velocity_msg(msg.data, rospy.get_rostime())
        #velocity_publisher.publish(msg)
    
    rospy.Subscriber('/youbot_base/velocity_instruction', array_msgs.msg.FloatArray, velocity_array_callback)
    
    def stop_manipulator():
        print('Shutting down')
        # Finally stop the robot
        msg = get_twist_velocity_msg(np.zeros(3), rospy.get_rostime())
        velocity_publisher.publish(msg)
        print('Signal stop sent')
        
    rospy.on_shutdown(stop_manipulator)
    while not rospy.is_shutdown():
        try:
            sys.stdout.write('\033[45m' + node_name + '$\033[0m ')
            evaled = eval(sys.stdin.readline())
            print(str(evaled))
            if evaled.__class__ in [tuple, list]:
                array = np.array(evaled)
                msg = get_twist_velocity_msg(array, rospy.get_rostime())
                velocity_publisher.publish(msg)
                print('Published velocity command: ' + str(array))
            else:
                print('\033[91mError: Unexpected command\033[0m')
                msg = get_twist_velocity_msg([0, 0, 0], rospy.get_rostime())
                velocity_publisher.publish(msg)
        except:
            print('\033[91mError: Unexpected error occurred \033[0m')
            msg = get_twist_velocity_msg([0, 0, 0], rospy.get_rostime())
            velocity_publisher.publish(msg)
    

def get_twist_velocity_msg(array, timeStamp=None):
    '''
    
    :param array:    float array with values to the base
    velocity in fwd, bwd, rotation
    '''
    
    msg = geometry_msgs.msg.Twist()
    if len(array)>=1:
        msg.linear.x = array[0]
        msg.linear.y = array[1]
    msg.linear.z = 0
    
    msg.angular.x = 0
    msg.angular.y = 0
    if len(array) >=2:
        msg.angular.z = array[2]
    
    return msg

if __name__ == '__main__':
    main(sys.argv)
