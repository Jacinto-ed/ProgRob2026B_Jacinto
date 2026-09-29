#include <chrono>
#include <memory>
#include <string>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

using namespace std::chrono_literals;

// Nodo que publica mensajes desde C++
class PublisherCpp : public rclcpp::Node
{
public:
    PublisherCpp() : Node("publisher_cpp"), contador_(0)
    {
        // Se crea el publisher usando el topic trafico_zmg
        publisher_ = this->create_publisher<std_msgs::msg::String>(
            "trafico_zmg", 10);

        // Cada segundo se genera y publica un mensaje nuevo
        timer_ = this->create_wall_timer(
            1s,
            [this]()
            {
                auto mensaje = std_msgs::msg::String();

                // El contador ayuda a identificar cada mensaje enviado
                mensaje.data =
                    "Mensaje desde C++ #" + std::to_string(contador_++);

                RCLCPP_INFO(
                    this->get_logger(),
                    "Publicando: %s",
                    mensaje.data.c_str());

                publisher_->publish(mensaje);
            });
    }

private:
    // Objetos necesarios para publicar y controlar el tiempo
    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
    rclcpp::TimerBase::SharedPtr timer_;
    int contador_;
};

int main(int argc, char * argv[])
{
    // Inicia ROS 2 y mantiene activo el nodo
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<PublisherCpp>());
    rclcpp::shutdown();

    return 0;
}