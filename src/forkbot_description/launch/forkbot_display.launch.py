from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from pathlib import Path
import xacro

# Configura la visualizacion del robot y los controles de sus articulaciones.
def generate_launch_description():
    ruta = Path(get_package_share_directory("forkbot_description")) / "urdf" / "forkbot.urdf.xacro"
    descripcion = xacro.process_file(str(ruta)).toxml()
    rviz_config = Path(get_package_share_directory("forkbot_description")) / "rviz" / "forkbot.rviz"

    return LaunchDescription([
        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            parameters=[{"robot_description": descripcion}]
        ),
        Node(
            package="joint_state_publisher_gui",
            executable="joint_state_publisher_gui"
        ),
        Node(
            package="rviz2",
            executable="rviz2",
            arguments=["-d", str(rviz_config)]
        )
    ])
