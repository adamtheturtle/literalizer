#include <cstddef>
#include <map>
#include <string>
#include <variant>
#include <vector>
int main() {
auto my_data = std::map<std::string, std::variant<std::nullptr_t, std::map<std::string, std::variant<std::vector<double>, bool>>>>{
    {"b", nullptr},
    {"a", std::map<std::string, std::variant<std::vector<double>, bool>>{{"y", std::vector<double>{1.0}}, {"x", false}}},
};
    (void)my_data;
    return 0;
}
