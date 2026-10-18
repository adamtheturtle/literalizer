#include <initializer_list>
#include <string>
#include <map>
#include <array>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::map<std::string, std::array<int, 3>>>{
    {"a", std::map<std::string, std::array<int, 3>>{{"b", std::array<int, 3>{1, 2, 3}}}},
};
    (void)my_data;
    return 0;
}
