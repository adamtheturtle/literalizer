#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
int main() {
const auto my_data = std::vector<std::map<std::string, std::variant<std::string, bool>>>{
    std::map<std::string, std::variant<std::string, bool>>{{"type", "create"}, {"pr_id", "pr_1"}, {"draft", true}},
    std::map<std::string, std::variant<std::string, bool>>{{"type", "create"}, {"pr_id", "pr_2"}},
};
(void)my_data;
my_data = std::vector<std::map<std::string, std::variant<std::string, bool>>>{
    std::map<std::string, std::variant<std::string, bool>>{{"type", "create"}, {"pr_id", "pr_1"}, {"draft", true}},
    std::map<std::string, std::variant<std::string, bool>>{{"type", "create"}, {"pr_id", "pr_2"}},
};
    (void)my_data;
    return 0;
}
