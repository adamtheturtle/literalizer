#include <initializer_list>
#include <string>
#include <map>
#include <variant>
int main() {
const auto my_data = std::map<std::string, std::variant<std::string, int, bool>>{
    // Server configuration
    {"host", "localhost"},  // default host
    {"port", 8080},
    // Enable debug mode
    {"debug", true},
};
    (void)my_data;
    return 0;
}
