import rclpy
from rclpy.node import Node
from std_msgs.msg import String


# Nodo encargado de publicar mensajes desde Python
class PublisherPy(Node):

    def __init__(self):
        super().__init__('publisher_py')

        # Publisher conectado al topic trafico_zmg
        self.publisher_ = self.create_publisher(
            String,
            'trafico_zmg',
            10
        )

        # Se ejecuta la funcion de publicacion cada segundo
        self.timer = self.create_timer(1.0, self.publicar_mensaje)
        self.contador = 0

    def publicar_mensaje(self):
        mensaje = String()

        # Se agrega un contador para distinguir los mensajes
        mensaje.data = f'Mensaje desde Python #{self.contador}'

        self.get_logger().info(
            f'Publicando: {mensaje.data}'
        )

        self.publisher_.publish(mensaje)
        self.contador += 1


def main(args=None):
    # Inicia ROS 2 y mantiene funcionando el nodo
    rclpy.init(args=args)

    nodo = PublisherPy()

    rclpy.spin(nodo)

    nodo.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()