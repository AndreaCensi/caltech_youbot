#!/usr/bin/env python
import roslib; roslib.load_manifest('youbot_agent')
import sys
import numpy as np
from sensor_msgs.msg import PointCloud, LaserScan
import rospy #@UnresolvedImport
import array_msgs.msg #@UnresolvedImport
roslib.load_manifest('laser_assembler')
from laser_assembler.srv import *

class Hokuyos2pc():

    def main(self, args, node_name='hokuyo2pc'):
        rospy.init_node(node_name)
        rospy.loginfo('Hokuyo2pcl started.')
        self.pub = rospy.Publisher('~cloud', PointCloud)
        assemble_scans = rospy.ServiceProxy('~assemble_scans', AssembleScans)
        while not rospy.is_shutdown():
            resp = assemble_scans(rospy.Time(0,0), rospy.get_rostime())
            print("Got cloud with %u points" % len(resp.cloud.points))
            self.pub.publish(resp.cloud)
            rospy.sleep(0.1)


def main(args):
    Hokuyos2pc().main(args)
   

if __name__ == '__main__':
    main(sys.argv)
