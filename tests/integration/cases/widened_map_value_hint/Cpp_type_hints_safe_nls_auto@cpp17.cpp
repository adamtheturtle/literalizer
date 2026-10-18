#include <initializer_list>
#include <string>
#include <cstddef>
#include <map>
#include <vector>
#include <variant>
int main() {
auto my_data = std::vector<std::variant<std::map<std::string, long>, long, std::string, bool, double, std::nullptr_t>>{
    std::map<std::string, long>{{"a", 1L}},
    1L,
    "x",
    true,
    2.5,
    nullptr,
};
    (void)my_data;
    return 0;
}
