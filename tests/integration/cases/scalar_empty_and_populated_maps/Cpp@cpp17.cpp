#include <cstddef>
#include <map>
#include <string>
#include <variant>
#include <vector>
int main() {
auto my_data = std::vector<std::variant<int, std::map<std::string, std::nullptr_t>, std::map<std::string, int>>>{
    1,
    std::map<std::string, std::nullptr_t>{},
    std::map<std::string, int>{{"x", 2}},
};
    (void)my_data;
    return 0;
}
