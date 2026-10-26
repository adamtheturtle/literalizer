#include <cstddef>
#include <map>
#include <string>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::variant<std::string, std::nullptr_t>>{
    {"host", "localhost"},
    {"port", nullptr},  // not configured yet
};
    (void)my_data;
    return 0;
}
