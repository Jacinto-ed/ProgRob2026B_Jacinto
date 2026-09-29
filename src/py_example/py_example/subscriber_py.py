import rclpy
from rclpy.node import Node
from std_msgs.msg import String


# Nodo que escucha los mensajes publicados en trafico_zmg
class SubscriberPy(Node):

    def __init__(self):
        super().__init__('subscriber_py')

        # Suscripcion al mismo topic de los dos publishers
        self.subscription = self.create_subscription(
            String,
            'trafico_zmg',
            self.recibir_mensaje,
            10
        )

    def recibir_mensaje(self, mensaje):
        # Cada mensaje recibido se muestra en la terminal
        self.get_logger().info(
            f'Recibido: {mensaje.data}'
        )


def main(args=None):
    # Inicia ROS 2 y deja al nodo esperando mensajes
    rclpy.init(args=args)

    nodo = SubscriberPy()

    rclpy.spin(nodo)

    nodo.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()