#include "youbot/YouBotBase.hpp"
#include "youbot/YouBotManipulator.hpp"
#include "ros/ros.h"
#include "std_msgs/String.h"
#include <sstream>

using namespace youbot;

/*void chatterCallback(const std_msgs::String::ConstPtr& msg)
{
  ROS_INFO("I heard: [%s]", msg->data.c_str());
}*/

int main(int argc, char **argv) {

    ros::init(argc, argv, "talker");
    /*
    ros::NodeHandle n;
    
    ros::Subscriber sub = n.subscribe("chatter", 1, chatterCallback);
    */

	LOG(info) << "My Demo";
	/* configuration flags for different system configuration (e.g. base without arm)*/
	bool youBotHasBase = false;
	bool youBotHasArm = false;

	/* define velocities */
	double translationalVelocity = 0.05; //meter_per_second
	double rotationalVelocity = 0.05; //radian_per_second

	/* create handles for youBot base and manipulator (if available) */
	YouBotBase* myYouBotBase = 0;
	YouBotManipulator* myYouBotManipulator = 0;

	try {
		myYouBotBase = new YouBotBase("youbot-base", YOUBOT_CONFIGURATIONS_DIR);
		myYouBotBase->doJointCommutation();

		youBotHasBase = true;
	} catch (std::exception& e) {
		LOG(warning) << e.what();
		youBotHasBase = false;
	}

	try {
		myYouBotManipulator = new YouBotManipulator("youbot-manipulator", YOUBOT_CONFIGURATIONS_DIR);
		myYouBotManipulator->doJointCommutation();
		myYouBotManipulator->calibrateManipulator();

		youBotHasArm = true;
	} catch (std::exception& e) {
		LOG(warning) << e.what();
		youBotHasArm = false;
	}

	/*
	* Variable for the base.
	* Here "boost units" is used to set values in OODL, that means you have to set a value and a unit.
	*/
	quantity<si::velocity> longitudinalVelocity = 0 * meter_per_second;
	quantity<si::velocity> transversalVelocity = 0 * meter_per_second;
	quantity<si::angular_velocity> angularVelocity = 0 * radian_per_second;

	/* Variable for the arm. */
	JointAngleSetpoint desiredJointAngle;
	if (youBotHasArm) {
		LOG(info) << "Arm found";
	}
	try {
		/*
		 * Simple sequence of commands to the youBot:
		 */

		//if (youBotHasBase) {
		if (false) {

			/* forward */
			longitudinalVelocity = translationalVelocity * meter_per_second;
			transversalVelocity = 0 * meter_per_second;
			myYouBotBase->setBaseVelocity(longitudinalVelocity, transversalVelocity, angularVelocity);
			LOG(info) << "drive forward";
			SLEEP_MILLISEC(2000);

			/* backwards */
			longitudinalVelocity = -translationalVelocity * meter_per_second;
			transversalVelocity = 0 * meter_per_second;
			myYouBotBase->setBaseVelocity(longitudinalVelocity, transversalVelocity, angularVelocity);
			LOG(info) << "drive backwards";
			SLEEP_MILLISEC(2000);

			/* left */
			longitudinalVelocity = 0 * meter_per_second;
			transversalVelocity = translationalVelocity * meter_per_second;
			angularVelocity = 0 * radian_per_second;
			myYouBotBase->setBaseVelocity(longitudinalVelocity, transversalVelocity, angularVelocity);
			LOG(info) << "drive left";
			SLEEP_MILLISEC(2000);

			/* right */
			longitudinalVelocity = 0 * meter_per_second;
			transversalVelocity = -translationalVelocity * meter_per_second;
			angularVelocity = 0 * radian_per_second;
			myYouBotBase->setBaseVelocity(longitudinalVelocity, transversalVelocity, angularVelocity);
			LOG(info) << "drive right";
			SLEEP_MILLISEC(2000);

			/* stop base */
			longitudinalVelocity = 0 * meter_per_second;
			transversalVelocity = 0 * meter_per_second;
			angularVelocity = 0 * radian_per_second;
			myYouBotBase->setBaseVelocity(longitudinalVelocity, transversalVelocity, angularVelocity);
			LOG(info) << "stop base";
		}

		if (youBotHasArm) {

			/* unfold arm 
			 * all of the following constants are empirically determined to move the arm into the desired position 
			 */
			/*LOG(info) << "first move, to start";
	        std::vector<JointAngleSetpoint> angles(5);
            angles[0].angle = 0.1 * radian;
            angles[1].angle = 0.1 * radian;
            angles[2].angle = -0.1 * radian;
            angles[3].angle = 0.1 * radian;
            angles[4].angle = 0.2 * radian;
            myYouBotManipulator->setJointData(angles);
            SLEEP_MILLISEC(4000);
            
	    	LOG(info) << "second move";
            //std::vector<JointAngleSetpoint> angles(5);
            angles[0].angle = 2.3 * radian;
            angles[1].angle = 0.3 * radian;
            angles[2].angle = -0.3 * radian;
            angles[3].angle = 0.3 * radian;
            angles[4].angle = 0.4 * radian;
            myYouBotManipulator->setJointData(angles);
            SLEEP_MILLISEC(1000);
            
		    LOG(info) << "last move, back to start";
            //std::vector<JointAngleSetpoint> angles(5);
            angles[0].angle = 0.1 * radian;
            angles[1].angle = 0.1 * radian;
            angles[2].angle = -0.1 * radian;
            angles[3].angle = 0.1 * radian;
            angles[4].angle = 0.2 * radian;
            myYouBotManipulator->setJointData(angles);
		    SLEEP_MILLISEC(1000);*/


			std::vector<JointVelocitySetpoint> velocity(5);
			velocity[0].angularVelocity = 0.2 * radian_per_second;
			velocity[1].angularVelocity = 0.20 * radian_per_second;
			velocity[2].angularVelocity = 0.20 * radian_per_second;
			velocity[3].angularVelocity = 0.20 * radian_per_second;
			velocity[4].angularVelocity = 0.2 * radian_per_second;
            myYouBotManipulator->setJointData(velocity);
		    SLEEP_MILLISEC(4000);

			velocity[0].angularVelocity = 0.00 * radian_per_second;
			velocity[1].angularVelocity = 0.00 * radian_per_second;
			velocity[2].angularVelocity = 0.00 * radian_per_second;
			velocity[3].angularVelocity = 0.00 * radian_per_second;
			velocity[4].angularVelocity = 0.00 * radian_per_second;
            myYouBotManipulator->setJointData(velocity);


    	    LOG(info) << "done";
	}

	} catch (std::exception& e) {
		std::cout << e.what() << std::endl;
		std::cout << "unhandled exception" << std::endl;
	}

	/* clean up */
	if (myYouBotBase) {
		delete myYouBotBase;
		myYouBotBase = 0;
	}
	if (myYouBotManipulator) {
		delete myYouBotManipulator;
		myYouBotManipulator = 0;
	}

	LOG(info) << "Done.";

    //ros::spin();

	return 0;
}
