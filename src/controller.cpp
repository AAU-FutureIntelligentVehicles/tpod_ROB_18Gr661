#include <iostream>
#include <cstring>
#include <ros/ros.h>
#include <std_msgs/Float64.h>
#include <std_msgs/Int8.h>
#include <eigen3/Eigen/Dense>
#include <cmath>
#include <geometry_msgs/Pose2D.h>

using namespace std;

#define K 0.4   //gain

//global variables that get updated when new information from the subsribers are gathered
float turningAngle = 0;
float isAvoidance = 0;
std_msgs::Float64 accelerator_position;

//Callback function updating global variables from the path planner
void updatePosition_cb(geometry_msgs::Pose2D point){
	turningAngle = point.theta;											//This is Theta Error. Turning angle received from the path point package.
	accelerator_position.data = 1;										//This is what we send to the golf cart accellerator. Having it in the callback makes sure we only drive, when we have started receiving points.
}

//Callback function updating the global variable if we are going to collide and we shoule brake.
void updateAvoidance_cb(std_msgs::Int8 isAvoidanceCallBack){
    if (isAvoidanceCallBack.data == 1) {
        isAvoidance = 1;												//If we receive 1 from the avoidance system we want to brake. Changing isAvoidance to 1 enters the loop for braking in main.
    }

	else if (isAvoidanceCallBack.data == 0){
		isAvoidance = 0;												//When the obstacle has been removed we want to drive again. Here we set isAvoidance to 0 to enter the loop for driving.
	}
}

int main(int argc, char **argv){

	//ROS stuff
	ros::init(argc, argv, "Controller");
   	ros::NodeHandle nh;

	//setting up subscriptions
	ros::Subscriber path_planner_sub = nh.subscribe("/path_point", 1, updatePosition_cb);
	//ros::Subscriber avoidance_sub = nh.subscribe("/avoid", 1, updateAvoidance_cb);
	isAvoidance = 0;		//for testing without obstacle avoidance

	//setting up the publishers and creating topics
	ros::Publisher set_steering_angle_pub = nh.advertise<std_msgs::Float64>("set_steering_angle", 1000);
	ros::Publisher set_brake_position_pub = nh.advertise<std_msgs::Float64>("set_brake_position", 1000);
	ros::Publisher set_accelerator_position_pub = nh.advertise<std_msgs::Float64>("set_accelerator_position", 1000);

	//for publishing
	std_msgs::Float64 turn_ticks;
    std_msgs::Float64 brake_position;
	accelerator_position.data = 0;


	while(ros::ok()){

		if (isAvoidance == 0){									//Loop for driving when no obstacle is in front of us

			//convert the angle to ticks
			float beta = turningAngle * K * 43408.5889;

			//safety stuff so we dont turn the steering wheel more than the car is physically capable of
			if (beta >= 22000){
				beta = 22000;
			}
			else if (beta <= -22000){
				beta = -22000;
			}

			cout << beta << endl;												//Outputting what we want to turn

			turn_ticks.data = beta;												//This is what we publish to the steering wheel
			brake_position.data = 2.4;											//When brake is set to 2.4 we are not braking

			//Here we do the actual publishing
			set_steering_angle_pub.publish(turn_ticks);
			set_accelerator_position_pub.publish(accelerator_position);
			set_brake_position_pub.publish(brake_position);

			ros::spinOnce();													//updates subsribers

			usleep(10000);														//Waits some time
		}

		else if (isAvoidance == 1){												//This is the loop for braking, when an obstacle is in front of us.
		brake_position.data = 0;												//we want to publish 0 to the brake = we start braking maximum
		accelerator_position.data = 0;											//we want to send 0 to the accelerator = we stop applying speed

		//Here we do the actual publishing for braking
		set_brake_position_pub.publish(brake_position);
		set_accelerator_position_pub.publish(accelerator_position);

		ros::spinOnce();														//updates subsribers

		}

	}
}
