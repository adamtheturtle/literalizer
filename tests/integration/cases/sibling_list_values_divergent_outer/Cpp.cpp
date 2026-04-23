#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
void check_() {
auto my_data = std::map<std::string, std::variant<std::vector<int>, std::vector<std::string>>>{
    {"a", std::vector<int>{1}},
    {"b", std::vector<std::string>{"x"}},
};
}
