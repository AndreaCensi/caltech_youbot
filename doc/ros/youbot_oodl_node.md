# Node [/youbot_oodl_driver]

If succesfully initialized, the ros node will have the following interfaces:

### Publications: 
 * /joint_states [sensor_msgs/JointState]
 * /rosout [rosgraph_msgs/Log]
 * /tf [tf/tfMessage]
 * /odom [nav_msgs/Odometry]

### Subscriptions: 
 * /arm_1/gripper_controller/position_command [unknown type]
 * /arm_1/arm_controller/position_command [unknown type]
 * /cmd_vel [unknown type]
 * /arm_1/arm_controller/velocity_command [unknown type]

### Services: 
 * /reconnect
 * /base/switchOffMotors
 * /arm_1/switchOnMotors
 * /youbot_oodl_driver/get_loggers
 * /arm_1/switchOffMotors
 * /arm_1/calibrate
 * /base/switchOnMotors
 * /youbot_oodl_driver/set_logger_level

### Connections:
 * topic: /rosout
    * to: /rosout
    * direction: outbound
    * transport: TCPROS
 
## Ros Node Rate

The rate for the youbot_oodl_node is currently hardcoded to 50Hz in youbot_oodl.cpp. 
There is currently no service to change the rate on the run and there is no functionality to specify the rate at startup.
The YouBot controller can take commands witha frecuency of 1kHz.
 
![rxgraph](images/youbot_oodl_driver_rxgraph.png)

## Controller Messages
### velocity_command
Commands a velocity to the robot. 

  Message type:      `brics_actuator.msg.JointVelocities()`
  
  Message properties:
  
    poisonStamp: 
      originator: ''
      description: ''
      qos: 0.0
    velocities: []
    
  velocities contains an array with `brics_actuator.msg.JointValue()` messages. each `JointValue()` message specifies the velocity of one joint. It has the properties:
  
    timeStamp: 
      secs: 0
      nsecs: 0
    joint_uri: ''
    unit: ''
    value: 0.0
    
  * joint_uri specifies the name of the joint. The uris for the manipulator joints are 'arm_joint_1', ..., 'arm_joint_5'
  * unit specifies the units of the value by a string. Possible values in python are:
    - `'s^-1 rad'` radians per second
    - TODO: complete list
  * value specifies the velocity value.
