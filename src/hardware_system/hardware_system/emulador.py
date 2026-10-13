import rclpy
from rclpy.node import Node
from robx7_interfaces.msg import HardwareStatus


class EmuladorHardware(Node):

    def __init__(self):
        super().__init__('emulador_node')

        # Creamos el publicador de los datos del hardware
        self.publisher = self.create_publisher(
            HardwareStatus, 'hardware_status', 10
        )

        # Diferentes estados para simular el funcionamiento
        self.estados = [
            (40, True, 'Operacion normal'),
            (48, True, 'Operacion normal'),
            (58, True, 'Calentando'),
            (78, True, 'Temperatura alta'),
            (90, False, 'Fallo de sensor'),
            (65, True, 'Enfriando')
        ]

        self.contador = 0

        # Publicamos un mensaje cada segundo
        self.timer = self.create_timer(1.0, self.publicar)

    def publicar(self):
        temperatura, motores, estado = self.estados[
            self.contador % len(self.estados)
        ]

        mensaje = HardwareStatus()
        mensaje.temperatura = temperatura
        mensaje.motores_listos = motores
        mensaje.debug_msg = estado

        self.publisher.publish(mensaje)

        self.get_logger().info(
            f'Temperatura: {temperatura} | '
            f'Motores: {motores} | Estado: {estado}'
        )

        self.contador += 1


def main(args=None):
    rclpy.init(args=args)

    nodo = EmuladorHardware()
    rclpy.spin(nodo)

    nodo.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
