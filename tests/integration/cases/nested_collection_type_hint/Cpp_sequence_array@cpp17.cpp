#include <initializer_list>
#include <string>
#include <map>
#include <array>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::array<std::map<std::string, int>, 1>>{
    {"a", std::array<std::map<std::string, int>, 1>{std::map<std::string, int>{{"b", 1}}}},
};
    (void)my_data;
    return 0;
}
