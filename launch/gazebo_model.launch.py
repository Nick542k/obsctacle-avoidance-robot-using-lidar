import os
import xacro

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription

from launch.launch_description_sources import (
    PythonLaunchDescriptionSource
)

from launch_ros.actions import Node


def generate_launch_description():

    # --------------------------------------------------
    # Names
    # --------------------------------------------------

    robot_name = "differential_drive_robot"

    package_name = "mobile_robot"

    # --------------------------------------------------
    # Files
    # --------------------------------------------------

    model_file = os.path.join(
        get_package_share_directory(package_name),
        "model",
        "robot.xacro"
    )

    world_file = os.path.join(
        get_package_share_directory(package_name),
        "model",
        "empty_world.world"
    )

    bridge_params = os.path.join(
        get_package_share_directory(package_name),
        "parameters",
        "bridge_parameters.yaml"
    )

    # --------------------------------------------------
    # Xacro
    # --------------------------------------------------

    robot_description = xacro.process_file(
        model_file
    ).toxml()

    # --------------------------------------------------
    # Gazebo
    # --------------------------------------------------

    gazebo = IncludeLaunchDescription(

        PythonLaunchDescriptionSource(

            os.path.join(

                get_package_share_directory(
                    "gazebo_ros"
                ),

                "launch",
                "gazebo.launch.py"

            )

        ),

        launch_arguments={
            "world": world_file
        }.items()

    )

    # --------------------------------------------------
    # Bridge
    # --------------------------------------------------

    bridge = Node(

        package="ros_gz_bridge",

        executable="parameter_bridge",

        arguments=[
            "--ros-args",
            "-p",
            f"config_file:={bridge_params}"
        ],

        output="screen"

    )

    # --------------------------------------------------
    # Robot State Publisher
    # --------------------------------------------------

    robot_state_publisher = Node(

        package="robot_state_publisher",

        executable="robot_state_publisher",

        output="screen",

        parameters=[

            {
                "robot_description":
                robot_description,

                "use_sim_time": True
            }

        ]

    )

    # --------------------------------------------------
    # Spawn Robot
    # --------------------------------------------------

    spawn_robot = Node(

        package="gazebo_ros",

        executable="spawn_entity.py",

        arguments=[

            "-topic",
            "robot_description",

            "-entity",
            robot_name

        ],

        output="screen"

    )

    # --------------------------------------------------
    # Launch
    # --------------------------------------------------

    return LaunchDescription([

        gazebo,

        bridge,

        robot_state_publisher,

        spawn_robot

    ])
