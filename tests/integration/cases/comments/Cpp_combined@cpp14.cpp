#include <initializer_list>
#include <string>
#include <map>
template <typename... Types> struct LiteralizerVariant { template <typename T> LiteralizerVariant(T&&) {} };
int main() {
auto my_data = std::map<std::string, LiteralizerVariant<std::string, int, bool>>{
    // Server configuration
    {"host", "localhost"},  // default host
    {"port", 8080},
    // Enable debug mode
    {"debug", true},
};
(void)my_data;
my_data = std::map<std::string, LiteralizerVariant<std::string, int, bool>>{
    // Server configuration
    {"host", "localhost"},  // default host
    {"port", 8080},
    // Enable debug mode
    {"debug", true},
};
    (void)my_data;
    return 0;
}
