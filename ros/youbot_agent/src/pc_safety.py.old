#!/usr/bin/env python
import roslib; roslib.load_manifest('youbot_agent')
import sys
import numpy as np
from sensor_msgs.msg import PointCloud
import rospy #@UnresolvedImport
import array_msgs.msg #@UnresolvedImport
roslib.load_manifest('laser_assembler')
from laser_assembler.srv import *
import time

class PCSafety():

    def main(self, args, node_name='pc_safety'):
        rospy.init_node(node_name)
        rospy.loginfo('PCSafety started.')
        
        self.pub = rospy.Publisher('~cloud', PointCloud)
        rospy.loginfo('Looking for service')
        assemble_scans = rospy.ServiceProxy('~assemble_scans', AssembleScans)
        rospy.loginfo('...found')

        while not rospy.is_shutdown():
            interval = 5
            from_time = rospy.Time.from_sec(time.time()-interval)
            to_time = rospy.Time.from_sec(time.time())
            resp = assemble_scans(from_time, to_time)
            s = "Got cloud with %u points" % len(resp.cloud.points)
            print(s)
            rospy.loginfo(s)
            self.pub.publish(resp.cloud)
            rospy.sleep(0.1)

        # self.sub1 = rospy.Subscriber('/scan_hokuyo_H1204906', LaserScan, 
        #                              self.arrived)
        # self.sub2 = rospy.Subscriber('/scan_hokuyo_H1205005', LaserScan, 
        #                                 self.arrived)

    # def arrived(self, msg):
    #     print msg.__dict__.keys()
    #     max_angle = msg.angle_max
    #     ranges = np.array(msg.ranges)
    #     angles = np.arange(msg.angle_min, msg.angle_max, msg.angle_increment)
    #     #Filter out noise(<0.003), points >1m, leaves obstacles
    #     #near_angles = np.extract(np.logical_and(ranges<1, ranges>0.003),
    #     #                         angles)
    #     #near_ranges = np.extract(np.logical_and(ranges<1, ranges>0.003),
    #     #                         ranges)
        # print ranges[:20]

    # position_publisher = rospy.Publisher('/arm_1/arm_controller/position_command', brics_actuator.msg.JointPositions)

    # def msg_arrived(msg):
    #     rospy.loginfo('callback, received array %s' % msg)
    #     # print('callback')
    #     # print('Received array ' + str(msg.data))
    #     msg = get_joint_position_msg(msg.data, rospy.get_rostime())
    #     position_publisher.publish(msg)
    
    # rospy.Subscriber('/youbot_arm/position_instruction', array_msgs.msg.FloatArray, position_array_callback)
    
    # def stop_manipulator():
    #     rospy.logerr('Sending stop signal (zero velocity) to robot arm')
    #     msg = get_joint_velocity_msg(np.zeros(5), rospy.get_rostime())
    #     velocity_publisher.publish(msg)
        
    # rospy.on_shutdown(stop_manipulator)

    


def main(args):
    PCSafety().main(args)

if __name__ == '__main__':
    main(sys.argv)
