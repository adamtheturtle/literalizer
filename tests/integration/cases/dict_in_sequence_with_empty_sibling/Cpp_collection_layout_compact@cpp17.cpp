#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <cstddef>
#include <variant>
int main() {
auto my_data = std::vector<std::variant<std::map<std::string, int>, std::vector<std::nullptr_t>>>{
    std::map<std::string, int>{{"a", 1}},
    std::vector<std::nullptr_t>{},
};
    (void)my_data;
    return 0;
}
