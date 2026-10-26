#include <map>
#include <string>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::variant<std::string, int>>{
    // Configuration
    {"name", "app"},
    // Port setting
    {"port", 3'000},
};
    (void)my_data;
    return 0;
}
