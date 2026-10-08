#include <initializer_list>
#include <string>
#include <cstddef>
#include <map>
#include <vector>
#include <variant>
int main() {
auto my_data = std::vector<std::variant<std::map<std::string, int>, int, std::string, bool, double, std::nullptr_t>>{
    std::map<std::string, int>{{"a", 1}},
    1,
    "x",
    true,
    2.5,
    nullptr,
};
    (void)my_data;
    return 0;
}
