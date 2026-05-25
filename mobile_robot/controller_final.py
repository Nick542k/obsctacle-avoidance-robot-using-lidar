import rclpy
from rclpy.node import Node

import numpy as np
import math
import time

from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from tf_transformations import euler_from_quaternion


TOPIC_CMD = '/cmd_vel'
TOPIC_ODOM = '/odom'
TOPIC_SCAN = '/scan'


class ControllerNode(Node):

    def __init__(
        self,
        xd,
        yd,
        ka,
        kr,
        ktheta,
        gstar,
        eps_orient,
        eps_control
    ):

        super().__init__('controller_node')

        self.xd = xd
        self.yd = yd

        self.ka = ka
        self.kr = kr
        self.ktheta = ktheta

        self.gstar = gstar

        self.eps_orient = eps_orient
        self.eps_control = eps_control

        self.odom_msg = Odometry()
        self.scan_msg = LaserScan()

        self.control_vel = Twist()

        self.create_subscription(
            Odometry,
            TOPIC_ODOM,
            self.pose_callback,
            10
        )

        self.create_subscription(
            LaserScan,
            TOPIC_SCAN,
            self.scan_callback,
            10
        )

        self.cmd_pub = self.create_publisher(
            Twist,
            TOPIC_CMD,
            10
        )

        self.timer = self.create_timer(
            0.05,
            self.control_function
        )

    def orientation_error(
        self,
        theta,
        theta_d
    ):

        error = theta_d - theta

        while error > np.pi:
            error -= 2*np.pi

        while error < -np.pi:
            error += 2*np.pi

        return error

    def pose_callback(
        self,
        msg
    ):

        self.odom_msg = msg

    def scan_callback(
        self,
        msg
    ):

        self.scan_msg = msg

    def control_function(self):

        x = self.odom_msg.pose.pose.position.x
        y = self.odom_msg.pose.pose.position.y

        quat = self.odom_msg.pose.pose.orientation

        q = [
            quat.x,
            quat.y,
            quat.z,
            quat.w
        ]

        _, _, theta = euler_from_quaternion(q)

        vector_goal = np.array([
            [x - self.xd],
            [y - self.yd]
        ])

        attractive_force = -self.ka * vector_goal

        repulsive_force = np.array([
            [0.0],
            [0.0]
        ])

        ranges = np.array(self.scan_msg.ranges)

        if len(ranges) > 0:

            valid = np.where(
                np.isfinite(ranges)
            )[0]

            for i in valid:

                distance = ranges[i]

                if distance < self.gstar:

                    angle = (
                        self.scan_msg.angle_min
                        + i*self.scan_msg.angle_increment
                        + theta
                    )

                    xo = x + distance*np.cos(angle)
                    yo = y + distance*np.sin(angle)

                    g = math.sqrt(
                        (x-xo)**2
                        +
                        (y-yo)**2
                    )

                    if g > 0:

                        gain = (
                            self.kr
                            *
                            (
                                (1/self.gstar)
                                -
                                (1/g)
                            )
                            /
                            (g**3)
                        )

                        repulsive_force += gain*np.array([
                            [x-xo],
                            [y-yo]
                        ])

        force = attractive_force - repulsive_force

        theta_d = math.atan2(
            force[1,0],
            force[0,0]
        )

        e_theta = self.orientation_error(
            theta,
            theta_d
        )

        dist_goal = np.linalg.norm(
            vector_goal
        )

        if dist_goal < self.eps_control:

            linear = 0.0
            angular = 0.0

        else:

            angular = (
                self.ktheta
                *
                e_theta
            )

            if abs(e_theta) > self.eps_orient:

                linear = 0.0

            else:

                linear = np.linalg.norm(force)

        linear = min(linear,2.5)

        self.control_vel.linear.x = linear
        self.control_vel.angular.z = angular

        self.cmd_pub.publish(
            self.control_vel
        )


def main(args=None):

    rclpy.init(args=args)

    node = ControllerNode(
        xd=10.0,
        yd=-10.0,
        ka=0.3,
        kr=10.0,
        ktheta=4.0,
        gstar=4.0,
        eps_orient=np.pi/10,
        eps_control=0.2
    )

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()