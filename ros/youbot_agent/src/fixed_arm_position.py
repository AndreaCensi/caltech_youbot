#!/usr/bin/env python

import roslib; roslib.load_manifest('youbot_agent')

import rospy #@UnresolvedImport
import brics_actuator.msg #@UnresolvedImport
import sys
import numpy as np

import array_msgs.msg #@UnresolvedImport

from position_joint_control import get_joint_position_msg
"""
    Use like this:
        
        rosrun youbot_agent fixed_arm_position.py _position:=look_up

"""

def main(args):
    rospy.init_node('fixed_arm_position')
    
    positions = {
        'look_forward': [3.14, 1, -2.4, 0.2, 3],
        'look_up':  [2.95, 0.015, -0.02, 0.36, 2.93],
    }

    value = rospy.get_param('~position', None)
    rospy.loginfo('Setting position %r' % value)
    if value is None:
        msg = 'Please set "position" to one of: %s.' % positions.keys()
        rospy.logerr(msg)
        return

    if not value in positions:
        msg = 'Given %r, not one of %s.' % (value, positions.keys())
        rospy.logerr(msg)
        return 

    repeat = rospy.get_param('~repeat', False)

    array = np.array(positions[value])

    position_publisher = rospy.Publisher('/arm_1/arm_controller/position_command', 
                                         brics_actuator.msg.JointPositions)


    while not rospy.is_shutdown():
        msg = get_joint_position_msg(array, rospy.get_rostime())
        position_publisher.publish(msg)    
        rospy.loginfo('Published position command: ' + str(msg))
        rospy.sleep(1.0)
        if not repeat:
            break


if __name__ == '__main__':
    main(sys.argv)
