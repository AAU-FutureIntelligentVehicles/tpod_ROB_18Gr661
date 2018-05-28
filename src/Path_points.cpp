#include "ros/ros.h"
#include <std_msgs/Float64.h>
#include <std_msgs/Float64MultiArray.h>
#include "geometry_msgs/Pose2D.h"
#include "vector"
#include "math.h"
#include <string>
#include "stdio.h"

#define LOWER_DIST 3.2                //The distance the cart look ahead is between 3.2 and 3.6 meters
#define UPPER_DIST 3.6                  //not used in current implementation
#define WHEEL_ANGLE 1.57         //90 degrees viewing angle
#define WHEEL_BASE 1.64               //The wheelbase length


class SubscriberAndPublisher
{
public:
    //constructor
    SubscriberAndPublisher()
    {
        //setting up subscriptions
        location_point_sub = n.subscribe("point_in",1,&SubscriberAndPublisher::Path_Point_Pub_CB,this);

        //setting up the publishers and creating topics
        point_pub = n.advertise<geometry_msgs::Pose2D>("path_point",1);
    };



    //whenever a point is received, this function checks if a point on the path is within the search space, if it is it calculated theta_error and sends it to the controller.
    void Path_Point_Pub_CB(const geometry_msgs::Pose2D path_points)
    {
      
        float alpha =  atan2(path_points.y,path_points.x)  ;                            //formula for finding an angle between two vectors

        if(path_points.x==0&&path_points.y==0)
        {
            solution.theta = 1000;
            point_pub.publish(solution);
        }
        else 
        {
            solution.theta = alpha;
            point_pub.publish(solution);
        }
        return;
    }
                





private:

//Ros stuff
    ros::NodeHandle n;

//setting up subscriptions
    ros::Subscriber location_point_sub;
//publisher
    ros::Publisher point_pub;

    //geometry_msgs::Pose2D path_points;
    //geometry_msgs::Pose2D last_point;
    geometry_msgs::Pose2D solution;
};

int main(int argc, char **argv){

    //Ros stuff
    ros::init(argc,argv,"path_points");
    ros::NodeHandle nh;
    SubscriberAndPublisher sap;
    ros::spin();
}
