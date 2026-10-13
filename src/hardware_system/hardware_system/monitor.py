import rclpy
from rclpy.node import Node
from robx7_interfaces.msg import HardwareStatus
from robx7_interfaces.srv import CheckSystem


class MonitorHardware(Node):

    def __init__(self):
        super().__init__('monitor_node')

        # Configuramos la temperatura maxima permitida
        self.declare_parameter('umbral_temperatura', 50)
        self.umbral = self.get_parameter('umbral_temperatura').value

        self.ultimo_estado = None

        # Recibimos los mensajes del emulador
        self.subscription = self.create_subscription(
            HardwareStatus,
            'hardware_status',
            self.recibir_datos,
            10
        )

        # Servicio para consultar si el robot puede operar
        self.servicio = self.create_service(
            CheckSystem,
            'check_system',
            self.verificar_sistema
        )

        self.get_logger().info(
            f'Monitor iniciado. Limite de temperatura: {self.umbral}'
        )

    def recibir_datos(self, mensaje):
        self.ultimo_estado = mensaje

        # Revisamos temperatura y motores
        if mensaje.temperatura > self.umbral:
            self.get_logger().warning(
                f'Temperatura alta: {mensaje.temperatura}'
            )

        if not mensaje.motores_listos:
            self.get_logger().warning(
                'Los motores no estan listos'
            )

    def verificar_sistema(self, solicitud, respuesta):

        if not solicitud.verificar:
            respuesta.seguro = False
            respuesta.mensaje = 'Verificacion no solicitada'

        elif self.ultimo_estado is None:
            respuesta.seguro = False
            respuesta.mensaje = 'Sin datos del hardware'

        else:
            temperatura = self.ultimo_estado.temperatura
            motores = self.ultimo_estado.motores_listos

            respuesta.seguro = (
                temperatura <= self.umbral and motores
            )

            if respuesta.seguro:
                respuesta.mensaje = 'Autorizacion de movimiento concedida'
            else:
                respuesta.mensaje = 'Bloqueo por temperatura o motores'

        self.get_logger().info(respuesta.mensaje)
        return respuesta


def main(args=None):
    rclpy.init(args=args)

    nodo = MonitorHardware()
    rclpy.spin(nodo)

    nodo.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
