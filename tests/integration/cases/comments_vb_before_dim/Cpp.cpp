#include <initializer_list>
#include <string>
#include <map>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::variant<std::string, int>>{
    // Configuration
    {"name", "app"},
    // Port setting
    {"port", 3000},
};
    (void)my_data;
    return 0;
}
