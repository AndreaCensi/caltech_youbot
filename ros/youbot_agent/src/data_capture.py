#!/usr/bin/env python
import roslib; roslib.load_manifest('youbot_agent')

import sensor_msgs.msg #@UnresolvedImport
import array_msgs.msg #@UnresolvedImport
import rospy #@UnresolvedImport
import Queue
import pdb

class DataCapture():
    def __init__(self):
        self.rate = 1
        node_name = 'youbot_velocity_control'
        rospy.init_node(node_name)
        print('Node starting')
        self.learning_publisher = rospy.Publisher('/learning_data', array_msgs.msg.LearningData)
        
        rospy.Subscriber('/usb_cam/image_raw', sensor_msgs.msg.Image, self.image_callback)
        rospy.Subscriber('/youbot/velocity_instruction', array_msgs.msg.FloatArray, self.command_callback)
        
        self.active_command = None
        self.image_queue = Queue.Queue(5)
        
        rospy.spin()
        
    def command_callback(self, msg):
        print('command_callback')
        self.active_command = msg
        self.image_queue = Queue.Queue(5)
        pdb.set_trace()
        
    def image_callback(self, msg):
        if self.image_queue.full():
            old_image = self.image_queue.get()
            
            self.image_queue.put(msg)
            data = array_msgs.msg.LearningData()
            data.Y0 = old_image
            data.Y1 = msg
            if self.active_command is not None:
                data.U_float = self.active_command
            
                print('\033[89mPublishing learning data \033[0m')
#            print(str(data))
                self.image_queue = Queue.Queue(5)
#                pdb.set_trace()
                self.learning_publisher.publish(data)
        else:
            print('Filling up queue')
            self.image_queue.put(msg)
        
if __name__ == '__main__':
    DataCapture()