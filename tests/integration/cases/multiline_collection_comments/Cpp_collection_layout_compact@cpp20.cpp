#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::variant<std::vector<int>, int>>{
    {"a", std::vector<int>{1, 2, 3}},  // inline a
    {"b", 2},  // inline b
};
    (void)my_data;
    return 0;
}
