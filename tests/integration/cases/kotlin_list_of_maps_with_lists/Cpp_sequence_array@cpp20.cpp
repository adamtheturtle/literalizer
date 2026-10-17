#include <initializer_list>
#include <string>
#include <map>
#include <array>
#include <variant>
int main() {
auto my_data = std::array<std::map<std::string, std::array<int, 1>>, 2>{
    std::map<std::string, std::array<int, 1>>{{"a", std::array<int, 1>{1}}},
    std::map<std::string, std::array<int, 1>>{{"a", std::array<int, 1>{2}}},
};
    (void)my_data;
    return 0;
}
