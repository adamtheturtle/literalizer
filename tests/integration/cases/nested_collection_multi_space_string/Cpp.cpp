#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
int main() {
const auto my_data = std::vector<std::map<std::string, std::variant<std::string, int>>>{
    std::map<std::string, std::variant<std::string, int>>{{"key", "hello   world"}, {"value", 1}},
};
    (void)my_data;
    return 0;
}
