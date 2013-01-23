# How to create a ROS package for the YouBot

1. Create the basic ROS package structure using roscreate-pkg.

usage:

    roscreate-pkg <package-name> [dependent-packages]
    
e.g. 

    roscreate-pkg youbot_demo youbot_driver roscpp rospy
    
This will createthe basic folder structure like:

    youbot@youbot:/opt/ros/electric/ros/ros$ ls youbot_demo/
    CMakeLists.txt  include  mainpage.dox  Makefile  manifest.xml  src

2. Replace the CMakeLists.txt with the code from the youbot_oodl package.


    
