from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([

        # Nodo que simula los datos del hardware
        Node(
            package='hardware_system',
            executable='emulador',
            output='screen'
        ),

        # Monitor con limite de temperatura de 75 grados
        Node(
            package='hardware_system',
            executable='monitor',
            parameters=[{'umbral_temperatura': 75}],
            output='screen'
        ),

        # Operador que consulta el estado del sistema
        Node(
            package='hardware_system',
            executable='operador',
            output='screen'
        )

    ])
