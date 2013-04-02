#!/usr/bin/env python
import roslib; roslib.load_manifest('youbot_agent')
import sys
import numpy as np
import yaml

import rospy #@UnresolvedImport
import array_msgs.msg #@UnresolvedImport

from youbot_agent.msg import Safety
from rospy import ROSException

from constraints import *

from geometry_msgs.msg import Twist


class GenericSafety():
    """ 
        Params:

            ~check_period
            ~info_period

        Input:
            ~safety  (msg, Safety)

    """
    def main(self, args, node_name='youbot_safety'):
        rospy.init_node(node_name)
        rospy.loginfo('Started.')

        self.safe_interval = rospy.Duration(1)

        # params
        self.check_period = rospy.get_param('~check_period', 0.1)
        self.info_period = rospy.get_param('~info_period', 10)
        
        # state
        self.checks = {}
        self.currently_safe = True

        self.define_events()

        # initialize
        rospy.spin()

    def define_events(self):
        rospy.Subscriber('~safety', Safety, self.safety_callback)
        rospy.Timer(rospy.Duration(self.check_period), self.periodic_callback)
        rospy.Timer(rospy.Duration(self.info_period), self.info_callback)


    def is_safe(self):
        return self.currently_safe

    def repeat_unsafe(self, desc):
        #rospy.loginfo('    unsafe: %s' % desc)
        pass

    def transition_unsafe(self, desc):
        rospy.loginfo('NOW unsafe: %s' % desc)

    def transition_safe(self):
        rospy.loginfo('now safe')

    def is_twist_safe(self, twist):
        """ Checks that the given twist command would be safe to execute.
            Returns a bool, and an explanation string.
        """
        # Let's go through the list and accumulate all constraints
        constraints = self.collect_constraints()
        return constraints_respected_by_twist(constraints, twist)

    def collect_constraints(self):
        """ Returns a list of dictionaries """
        constraints = []
        for id_check, check in self.checks.items():
            constraints.extend(self.get_constraints(id_check, check))
        return constraints

    def get_constraints(self, id_check, check):
        """ Returns a list of dictionaries """
        # first let's check for time
        interval = rospy.Time.now() - check['stamp']
        recent = interval < self.safe_interval
        if not recent:
            return [constraint_none(desc='%s expired: %s' % (id_check, interval))]
        return check['constraints']

    # callbacks

    def safety_callback(self, msg):
        id_check = msg.id_check
        safe = msg.safe
        desc = msg.desc
        stamp = msg.header.stamp
        constraints = yaml.load(msg.constraints)
        # print 'extra: %s' % extra

        if not id_check in self.checks:
            msg = 'First time we see check %r.' % id_check
            self.checks[id_check] = {}

        self.checks[id_check]['stamp'] = stamp
        self.checks[id_check]['desc'] = desc
        self.checks[id_check]['safe'] = safe
        self.checks[id_check]['constraints'] = constraints

    def info_callback(self, msg):
        constraints = self.collect_constraints()
        rospy.loginfo('constraints: %s' % constraints)

    def periodic_callback(self, msg):
        now_safe = True
        desc = ''
        # Let's go through the list
        for id_check, check in self.checks.items():
            interval = rospy.Time.now() - check['stamp']
            recent = interval < self.safe_interval

            if not recent:
                desc += '[%r: OLD %s]' % (id_check, interval)
                now_safe = False

            # if it's unsafe
            elif check['safe'] == False:
                desc += '[%s: %s]' % (id_check, check['desc'])
                now_safe = False

        change = self.currently_safe != now_safe
        self.currently_safe = now_safe
        if change:
            if now_safe:
                self.transition_safe()
            else:
                self.transition_unsafe(desc)

        if not now_safe:
            self.repeat_unsafe(desc)
 
    



class YoubotSafety(GenericSafety):

    @staticmethod
    def get_zero_twist():
        twist = Twist()
        twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
        twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
        return twist

    def cmd_vel_received(self, msg):
        twist = msg
        safe, why = self.is_twist_safe(twist)
        if safe:
            rospy.logdebug('Safe: passing over message')
            self.pub_cmd_vel.publish(msg)
        else: 
            msg_stop = YoubotSafety.get_zero_twist()
            rospy.loginfo('Suppressing unsafe:  %s' % why)
            self.pub_cmd_vel.publish(msg_stop)

    def define_events(self):
        GenericSafety.define_events(self)

        self.pub_cmd_vel = rospy.Publisher('~out_cmd_vel', Twist)
        rospy.Subscriber('~in_cmd_vel', Twist, self.cmd_vel_received)


def main(args):
    YoubotSafety().main(args)
   

if __name__ == '__main__':
    main(sys.argv)
