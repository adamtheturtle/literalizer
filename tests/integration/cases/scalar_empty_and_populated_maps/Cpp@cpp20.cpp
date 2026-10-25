#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <cstddef>
#include <variant>
int main() {
auto my_data = std::vector<std::variant<int, std::map<std::string, std::nullptr_t>, std::map<std::string, int>>>{
    1,
    std::map<std::string, std::nullptr_t>{},
    std::map<std::string, int>{{"x", 2}},
};
    (void)my_data;
    return 0;
}
