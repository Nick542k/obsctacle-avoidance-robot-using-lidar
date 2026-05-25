# Obstacle Avoidance Robot Using LiDAR

A ROS2 + Gazebo mobile robot simulation project that performs obstacle avoidance using LiDAR sensor data and Artificial Potential Field navigation.

---

## Project Overview

This project implements an autonomous differential drive mobile robot capable of:

- LiDAR based obstacle detection
- Obstacle avoidance using Artificial Potential Fields
- Goal based autonomous navigation
- ROS2 node architecture
- Gazebo simulation
- Differential drive control
- Odometry feedback localization

The robot moves toward a target position while avoiding obstacles detected by the LiDAR sensor.

---

## Features

- ROS2 Humble support
- Gazebo simulation environment
- LiDAR sensor integration
- Differential drive mobile robot
- Artificial Potential Field navigation
- Goal attraction force
- Obstacle repulsion force
- Odometry feedback
- RViz visualization

---

## ROS Topics

| Topic | Purpose |
|--------|----------|
| `/cmd_vel` | Velocity commands |
| `/scan` | LiDAR sensor data |
| `/odom1` | Robot odometry |
| `/odom1_tf` | Transform information |

---

## Navigation Algorithm

Artificial Potential Field Method:

### Attractive Force
Robot is pulled toward the target position.

### Repulsive Force
Nearby obstacles push the robot away.

Final movement force:

F = Attractive Force + Repulsive Force

The resultant vector determines:

- Linear velocity
- Angular velocity

---

## Dependencies

Install required ROS packages:

```bash
sudo apt update

sudo apt install ros-humble-gazebo-ros

sudo apt install ros-humble-ros-gz

sudo apt install ros-humble-tf-transformations
```

Install Python dependency:

```bash
pip install numpy
```

---

## Build

```bash
cd ~/mobile_ws

colcon build

source install/setup.bash
```

---

## Run Simulation

Launch Gazebo:

```bash
ros2 launch mobile_robot gazebo_model.launch.py
```

Run Controller:

```bash
ros2 run mobile_robot controller_final
```

---

## Project Structure

```
mobile_robot/

├── launch/
├── model/
├── parameters/
├── mobile_robot/
│   └── controller_final.py
├── package.xml
├── setup.py
└── README.md
```

---

## Future Improvements

- SLAM integration
- Path planning (A*)
- RRT planner
- Dynamic obstacle avoidance
- Nav2 integration
- Real robot deployment

---

## Technologies Used

- ROS2 Humble
- Gazebo
- Python
- LiDAR
- RViz2
- Differential Drive Kinematics

---

## Author

Nithish Kumar

Robotics and Automation Engineering

ROS2 • Gazebo • Autonomous Navigation

---

## License

Apache 2.0 License


## Screenshots
<img width="1495" height="790" alt="Screenshot from 2026-05-25 23-09-14" src="https://github.com/user-attachments/assets/ad030e7a-4c7e-401a-8ddc-3f470041a6e9" />
<img width="1154" height="806" alt="Screenshot from 2026-05-25 23-07-55" src="https://github.com/user-attachments/assets/0990451e-c60e-49e1-858e-051943b1d9e0" />

