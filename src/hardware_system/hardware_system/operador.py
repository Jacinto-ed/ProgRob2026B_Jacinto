import rclpy
from rclpy.node import Node
from robx7_interfaces.srv import CheckSystem


class OperadorHardware(Node):

    def __init__(self):
        super().__init__('operador_node')

        # Creamos el cliente para consultar al monitor
        self.cliente = self.create_client(
            CheckSystem, 'check_system'
        )

        self.pendiente = None

        # Consultamos el estado del robot cada 2 segundos
        self.timer = self.create_timer(
            2.0, self.consultar_sistema
        )

        self.get_logger().info('Operador iniciado')

    def consultar_sistema(self):

        # Revisamos si el servicio esta disponible
        if not self.cliente.service_is_ready():
            self.get_logger().warning(
                'Esperando al monitor...'
            )
            return

        # Evitamos enviar otra solicitud si hay una pendiente
        if self.pendiente is not None:
            return

        solicitud = CheckSystem.Request()
        solicitud.verificar = True

        # Enviamos la solicitud al monitor
        self.pendiente = self.cliente.call_async(solicitud)
        self.pendiente.add_done_callback(
            self.mostrar_respuesta
        )

    def mostrar_respuesta(self, futuro):

        try:
            respuesta = futuro.result()

            if respuesta.seguro:
                self.get_logger().info(
                    f'Sistema seguro: {respuesta.mensaje}'
                )
            else:
                self.get_logger().warning(
                    f'Sistema bloqueado: {respuesta.mensaje}'
                )

        except Exception as error:
            self.get_logger().error(
                f'Error al consultar: {error}'
            )

        finally:
            self.pendiente = None


def main(args=None):
    rclpy.init(args=args)

    nodo = OperadorHardware()
    rclpy.spin(nodo)

    nodo.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
