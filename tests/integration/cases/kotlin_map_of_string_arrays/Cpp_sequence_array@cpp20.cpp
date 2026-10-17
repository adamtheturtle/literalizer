#include <initializer_list>
#include <string>
#include <map>
#include <array>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::array<std::string, 1>>{
    {"a", std::array<std::string, 1>{"x"}},
    {"b", std::array<std::string, 1>{"y"}},
};
    (void)my_data;
    return 0;
}
