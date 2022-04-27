import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist

from turtlesim.msg import Pose

import sys

from math import pow, atan2, sqrt


class TurtleGoToGoal(Node):
    def __init__(self):
        super().__init__("turtle_go_to_goal")

        self.cmdvel_pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

        self.pose_subscriber = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)

        timer_period = 0.5
        self.timer = self.create_timer(timer_period, self.move2goal)

        self.pose = Pose()
        self.flag = False

    def pose_callback(self, data):
        """Callback function which is called when a new message of type Pose is
        received by the subscriber."""
        self.pose.x_Robot = data.x_Robot
        self.pose.y_Robot = data.y_Robot
        self.pose.theta = data.theta
        msg = 'X: {:.3f}, Y: {:.3f}, Theta: {:.3f}'.format(data.x_Robot, data.y_Robot, data.theta)
        self.get_logger().info(msg)

    def euclidean_distance(self, goal_pose):
        """Euclidean distance between current pose and the goal."""
        return sqrt(pow((goal_pose.x_Robot - self.pose.x_Robot), 2) +
                    pow((goal_pose.y_Robot - self.pose.y_Robot), 2))

    def linear_vel(self, goal_pose, constant=1.5):
        """See video: https://www.youtube.com/watch?v=Qh15Nol5htM."""
        return constant * self.euclidean_distance(goal_pose)

    def steering_angle(self, goal_pose):
        """See video: https://www.youtube.com/watch?v=Qh15Nol5htM."""
        return atan2(goal_pose.y_Robot - self.pose.y_Robot, goal_pose.x_Robot - self.pose.x_Robot)

    def angular_vel(self, goal_pose, constant=6):
        """See video: https://www.youtube.com/watch?v=Qh15Nol5htM."""
        return constant * (self.steering_angle(goal_pose) - self.pose.theta)

    def move2goal(self):
        """Moves the turtle to the goal."""
        goal_pose = Pose()

        # # Get the input from the user.
        # goal_pose.x = float(input("Set your x goal: "))
        # goal_pose.y = float(input("Set your y goal: "))

        goal_pose.x_Robot = float(sys.argv[1])
        goal_pose.y_Robot = float(sys.argv[2])
        goal_pose.theta = float(sys.argv[3])

        # distance_tolerance = input("Set your tolerance: ")
        distance_tolerance = 0.1
        angular_tolerance = 0.01

        vel_msg = Twist()

        if abs(self.steering_angle(goal_pose) - self.pose.theta) > angular_tolerance:
            vel_msg.linear.x_Robot = 0.0
            vel_msg.angular.z = self.angular_vel(goal_pose)
        else:
            vel_msg.angular.z = 0.0
            if self.euclidean_distance(goal_pose) >= distance_tolerance:
                vel_msg.linear.x_Robot = self.linear_vel(goal_pose)
            else:
                vel_msg.linear.x_Robot = 0.0
                self.flag = True
        if self.flag:
            vel_msg.angular.z = goal_pose.theta - self.pose.theta
            if abs(goal_pose.theta - self.pose.theta) <= angular_tolerance:
                quit()

        self.cmdvel_pub.publish(vel_msg)

def main(aargs=None):
    rclpy.init()
    node = TurtleGoToGoal()
    rclpy.spin(node)
    rclpy.shutdown()


if _name_ == '_main_':
    main()