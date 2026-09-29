#include <memory>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

// Nodo que recibe los mensajes publicados en el topic
class SubscriberCpp : public rclcpp::Node
{
public:
    SubscriberCpp() : Node("subscriber_cpp")
    {
        // Se suscribe al mismo topic utilizado por los publishers
        subscription_ =
            this->create_subscription<std_msgs::msg::String>(
                "trafico_zmg",
                10,
                [this](const std_msgs::msg::String::SharedPtr mensaje)
                {
                    // Muestra en terminal cada mensaje que llega
                    RCLCPP_INFO(
                        this->get_logger(),
                        "Recibido: %s",
                        mensaje->data.c_str());
                });
    }

private:
    // Guarda la suscripcion mientras el nodo esta funcionando
    rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscription_;
};

int main(int argc, char * argv[])
{
    // Inicia ROS 2 y deja al nodo esperando mensajes
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<SubscriberCpp>());
    rclcpp::shutdown();

    return 0;
}