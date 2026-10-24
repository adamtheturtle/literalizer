#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::variant<std::string, bool, std::vector<int>>>{
    {"name", "Ada"},
    {"active", true},
    {"scores", std::vector<int>{1, 2, 3}},
};
    (void)my_data;
    return 0;
}
