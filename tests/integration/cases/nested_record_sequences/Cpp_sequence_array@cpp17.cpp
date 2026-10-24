#include <initializer_list>
#include <string>
#include <map>
#include <array>
#include <variant>
int main() {
auto my_data = std::array<std::array<std::map<std::string, int>, 1>, 2>{
    std::array<std::map<std::string, int>, 1>{std::map<std::string, int>{{"a", 1}}},
    std::array<std::map<std::string, int>, 1>{std::map<std::string, int>{{"a", 2}}},
};
    (void)my_data;
    return 0;
}
