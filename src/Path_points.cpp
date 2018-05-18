#include "ros/ros.h"
#include <std_msgs/Float64.h>
#include <std_msgs/Float64MultiArray.h>
#include "geometry_msgs/Pose2D.h"
#include "vector"
#include "math.h"
#include <string>
#include "stdio.h"

#define LOWER_DIST 1.6                //The distance the cart look ahead is between 1.6 and 2 meter
#define UPPER_DIST 2                  //not used in current implementation
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
    void Path_Point_Pub_CB(const geometry_msgs::Pose2D::ConstPtr& path_points)
    {
        //if(path_points.empty())
        //{
        //    return;
        //}
        float alpha =  atan2(path_points.x,path_points.y)  ;                            //formula for finding an angle between two vectors

        if(path_points.x==0&&path_points.y==0)
        {
            solution.theta = 1000;
            point_pub.publish(solution);
        }
        else //if(alpha <= WHEEL_ANGLE/2) //alpha <= VIEWING_ANGLE/2){
        {
            solution.theta = alpha;
            point_pub.publish(solution);
        }
        return;
    }
                // set the solution
                //solution = path_points;
                //float determinant = car_vecx * p_vecy;// - car_vecy * p_vecx;                      //checking if the aiming vector is on the right hand side or left hand side. (should the cart turn right or left)
                //if (determinant < 0)
                //{
                //    solution.theta = -alpha;
                //}
                //else



        //    ++itter; // try the next point.
        //}

        //        std::cout<<"x =: "<<path_points.x<<"y ="<<path_points.y<<std::endl;
        //        return;}

        //for (auto itter = path_points)
        //{
        //calculate angle between cart vector and aiming vector
        //float dotprod = car_vecx * p_vecx; //+ car_vecy * p_vecy;                           //Finding the dotproduct between the two vectors
        //float norm_tpod = sqrt(car_vecx * car_vecx); //+ car_vecy * car_vecy);               //findin the length of the cart vector
        //float norm_itter = sqrt(p_vecx * p_vecx + p_vecy * p_vecy);                         //findin the length of the Aiming vector
        //float alpha = acos(dotprod/(norm_tpod*norm_itter));

        //float car_vecx = 1;                 //cos(theta)= 1
        //  float car_vecy = sin(theta) ;     because theta=0 and cart direction doesn't matter this cancels out.
        //float p_vecx = cos(path_points.x) ;
        //float p_vecy = sin(path_points.y) ;
        // is the angle within our viweing angle
    // we only get here if we went through the whole path
    // if there is only one point left we keep publishing a last point 1 m away from the last point
    // to ensure that the car drives all the way to the last path point.


    //else {
    //    ROS_INFO("There doesnt seem to be any path points within the bounds"); // if anything fails
    //    std::cout<<"\nThe next point is "<<path_points[1].x<<","<<path_points[1].y<<" | "<<path_points[1].theta<<std::endl;
    //}




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
