#include <cstddef>
#include <map>
#include <string>
#include <variant>
#include <vector>
int main() {
auto my_data = std::map<std::string, std::variant<std::vector<std::variant<int, std::string>>, std::vector<std::nullptr_t>>>{
    {"filled", std::vector<std::variant<int, std::string>>{1, "value"}},
    {"empty", std::vector<std::variant<int, std::string>>{}},
};
    (void)my_data;
    return 0;
}
