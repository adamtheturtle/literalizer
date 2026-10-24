#include <initializer_list>
#include <string>
#include <map>
#include <array>
#include <variant>
int main() {
auto shared = std::array<std::map<std::string, int>, 1>{
    std::map<std::string, int>{{"value", 1}},
};
auto my_data = std::array<std::array<std::map<std::string, int>, 1>, 2>{
    shared,
    shared,
};
    (void)my_data;
    return 0;
}
