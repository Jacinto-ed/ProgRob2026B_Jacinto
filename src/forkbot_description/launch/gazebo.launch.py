from pathlib import Path

import xacro
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    # Localizar el modelo Xacro de ForkBot.
    paquete = get_package_share_directory("forkbot_description")
    modelo = Path(paquete) / "urdf" / "forkbot.urdf.xacro"
    descripcion = xacro.process_file(str(modelo)).toxml()

    # Iniciar Gazebo con un mundo vacío y física activa.
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            str(Path(get_package_share_directory("ros_gz_sim"))
                / "launch" / "gz_sim.launch.py")
        ),
        launch_arguments={"gz_args": "-r empty.sdf"}.items()
    )

    # Publicar el modelo y sus transformaciones TF.
    publicador = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description": descripcion}],
        output="screen"
    )

    # Importar ForkBot desde /robot_description.
    insertar_robot = TimerAction(
        period=8.0,
        actions=[
            Node(
                package="ros_gz_sim",
                executable="create",
                arguments=[
                    "-topic", "/robot_description",
                    "-name", "forkbot",
                    "-z", "0.30"
                ],
                output="screen"
            )
        ]
    )

    return LaunchDescription([gazebo, publicador, insertar_robot])
