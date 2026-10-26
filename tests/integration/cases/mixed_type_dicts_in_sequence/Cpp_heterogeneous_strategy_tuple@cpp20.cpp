#include <map>
#include <string>
#include <variant>
#include <vector>
int main() {
auto my_data = std::vector<std::map<std::string, std::variant<std::string, bool>>>{
    std::map<std::string, std::variant<std::string, bool>>{{"type", "create"}, {"pr_id", "pr_1"}, {"draft", true}},
    std::map<std::string, std::variant<std::string, bool>>{{"type", "create"}, {"pr_id", "pr_2"}},
};
    (void)my_data;
    return 0;
}
