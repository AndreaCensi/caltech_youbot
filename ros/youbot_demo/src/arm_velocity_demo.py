#!/usr/bin/env python

import roslib; roslib.load_manifest('youbot_demo')

import rospy
import brics_actuator.msg
import sys
import pdb
import numpy as np

def main(args):
    node_name = 'youbot_arm_velocity_demo'
    rospy.init_node(node_name)
    print('Node started')
    velocity_publisher = rospy.Publisher('/arm_1/arm_controller/velocity_command', brics_actuator.msg.JointVelocities)
    
    def stop_manipulator():
        print('Shutting down')
        # Finally stop the robot
        msg = get_joint_velocity_msg(np.zeros(5), rospy.get_rostime())
        velocity_publisher.publish(msg)
        print('Signal stop sent')
    
    rospy.on_shutdown(stop_manipulator)
    
    t0 = rospy.get_time()
    T = 5  # Wave length
    
    ampl = np.array([.1, 0, 0, 0, 0])
    offs = np.array([1, 0, 0, 0, 0])
    
    pdb.set_trace()
    r = rospy.Rate(5)

    msg = get_joint_velocity_msg(ampl + offs)
    velocity_publisher.publish(msg)
    for _ in range(5):
        r.sleep()
    
    print('In position, starting the demo.')
    while not rospy.is_shutdown():
        t = rospy.get_time()
        array = ampl * np.sin((t - t0) * (2 * np.pi) / T)
        msg = get_joint_velocity_msg(array, rospy.Time.from_sec(t))
        
        print(array)
        velocity_publisher.publish(msg)
        r.sleep()
        
    
    
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
