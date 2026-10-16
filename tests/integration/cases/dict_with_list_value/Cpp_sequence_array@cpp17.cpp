#include <initializer_list>
#include <string>
#include <map>
#include <array>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::variant<std::string, std::array<int, 3>>>{
    {"name", "Alice"},
    {"scores", std::array<int, 3>{10, 20, 30}},
};
    (void)my_data;
    return 0;
}
