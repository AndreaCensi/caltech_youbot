# rosrun youbot_oodl start_youbot_oodl_driver

### Error:

    # rosrun youbot_oodl start_youbot_oodl_driver 
    [rospack] opendir error [No such file or directory] while crawling /home/youbot/ros_stacks_manual
    bash: command.txt: No such file or directory

### Solution
start drivers from launch file instead

    roslaunch youbot_oodl youbot_oodl_driver.launch
