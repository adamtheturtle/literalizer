#include <cstddef>
#include <map>
#include <string>
#include <variant>
#include <vector>
int main() {
auto my_data = std::vector<std::variant<std::map<std::string, int>, std::vector<std::nullptr_t>>>{
    std::map<std::string, int>{{"a", 1}},
    std::vector<std::nullptr_t>{},
};
    (void)my_data;
    return 0;
}
