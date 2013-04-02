#!/usr/bin/env python
import roslib; roslib.load_manifest('youbot_agent')

import rospy #@UnresolvedImport
import brics_actuator.msg #@UnresolvedImport
import sys
import numpy as np
import array_msgs.msg #@UnresolvedImport
import geometry_msgs.msg #@UnresolvedImport
from array_msgs.msg import FloatArray
from geometry_msgs.msg import Twist

def main(args):
    """
        out: ~cmd_vel
         in: ~cmd_array
    """
    rospy.init_node('array2twist')
    velocity_publisher = rospy.Publisher('~cmd_vel', Twist)
    
    def velocity_array_callback(msg):
        msg = get_twist_velocity_msg(msg.data, rospy.get_rostime())
        velocity_publisher.publish(msg)
    
    rospy.Subscriber('~cmd_array', FloatArray, velocity_array_callback)
    rospy.spin()

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
