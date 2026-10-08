#include <initializer_list>
#include <string>
#include <cstddef>
#include <map>
#include <vector>
#include <variant>
int main() {
auto actual = 42;
auto my_data = std::vector<std::variant<std::map<std::string, int>, std::map<std::string, std::nullptr_t>, int>>{
    std::map<std::string, int>{{"$ref", 1}},
    std::map<std::string, std::nullptr_t>{{"$ref", nullptr}},
    actual,
};
    (void)my_data;
    return 0;
}
