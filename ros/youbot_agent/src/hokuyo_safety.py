#!/usr/bin/env python
import roslib; roslib.load_manifest('youbot_agent')
import sys
import numpy as np
from sensor_msgs.msg import PointCloud
import rospy #@UnresolvedImport
import array_msgs.msg #@UnresolvedImport
roslib.load_manifest('laser_assembler')
from laser_assembler.srv import *
from youbot_agent.msg import Safety
from rospy import ROSException


class HokuyoSafety():
    """ 
        Every once in a while, this node 
        calls the assemblers to get a point cloud. 

        Input:
            ~assemble_scans0  (srv/AssembleScans)
            ~assemble_scans1  (srv/AssembleScans)

        Output:
            ~out_safe  (msg/PointCloud)
            ~out_unsafe  (msg/PointCloud)
            ~out_safety  (youtube_agent/Safety)
    """

    def main(self, args, node_name='hokuyo_safety'):
        rospy.init_node(node_name)
        rospy.loginfo('Started.')

        self.pub_safe = rospy.Publisher('~out_safe', PointCloud)
        self.pub_unsafe = rospy.Publisher('~out_unsafe', PointCloud)
        self.pub_safety = rospy.Publisher('~out_safety', Safety)

        names = ['~assemble_scans%d' % i for i in range(2)]
        self.init_services(names)

        while not rospy.is_shutdown():
            rospy.sleep(0.1)
            self.periodic()

    def periodic(self):
        warn_distance = rospy.get_param('~warn_distance', 0.7)

        clouds = self.get_clouds()            
        points = clouds[0].points + clouds[1].points
        frame_id = clouds[0].header.frame_id

        def norm(p):
            return np.hypot(np.hypot(p.x, p.y), p.z)

        p_safe = filter(lambda p: norm(p) > warn_distance, points)
        p_unsafe = filter(lambda p: norm(p) < warn_distance, points)

        pc_safe = PointCloud()            
        pc_safe.header.frame_id = frame_id
        pc_safe.points = p_safe
        self.pub_safe.publish(pc_safe)

        pc_unsafe = PointCloud()            
        pc_unsafe.header.frame_id = frame_id
        pc_unsafe.points = p_unsafe
        self.pub_unsafe.publish(pc_unsafe)


        if True and len(points) > 0:
            # find the closest point
            norms  = map(norm, points)
            closest = np.argmin(norms)
            p0 = points[closest]
            rospy.loginfo('Closest point is %s' % p0)

            extra = '{}'
        else:
            extra = '{}'

        msg_safety = Safety()
        msg_safety.id_check = 'hokuyo_safety'
        msg_safety.header.stamp = rospy.Time.now()
        
        if p_unsafe:
            msg_safety.safe = False
            msg_safety.desc = '%d unsafe points' % len(p_unsafe)
            msg_safety.extra = extra
        else:
            msg_safety.safe = True
            msg_safety.desc = 'OK' 
            msg_safety.extra = extra
        
        self.pub_safety.publish(msg_safety)


    def init_services(self, names , timeout=1):
        rospy.loginfo('Opening service proxies...')
        srv_assemble = []
        for n in names:
            rospy.wait_for_service(n, timeout=timeout)
            rospy.loginfo('Connecting to %s' % n)
            x = rospy.ServiceProxy(n, AssembleScans)
            rospy.loginfo('Connecting to %s [done]' % n)
            srv_assemble.append(x)
        self.services = srv_assemble

    def get_services(self):
        return self.services

    def get_clouds(self):
        clouds = []
        services = self.get_services()
        for i, srv in enumerate(services):
            resp = srv(rospy.Time(0,0), rospy.get_rostime())
            #rospy.loginfo('Cloud %d: %s points' %(i,  len(resp.cloud.points)))
            clouds.append(resp.cloud)
        return clouds
    


def main(args):
    HokuyoSafety().main(args)
   

if __name__ == '__main__':
    main(sys.argv)
