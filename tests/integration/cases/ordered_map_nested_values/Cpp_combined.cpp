#include <initializer_list>
#include <string>
#include <map>
#include <utility>
#include <vector>
#include <variant>
int main() {
const auto my_data = std::vector<std::pair<std::string, std::variant<std::string, std::map<std::string, std::string>>>>{
    {"name", "Alice"},
    {"scores", std::map<std::string, std::string>{{"1", "first"}, {"2", "second"}}},
};
(void)my_data;
my_data = std::vector<std::pair<std::string, std::variant<std::string, std::map<std::string, std::string>>>>{
    {"name", "Alice"},
    {"scores", std::map<std::string, std::string>{{"1", "first"}, {"2", "second"}}},
};
    (void)my_data;
    return 0;
}
