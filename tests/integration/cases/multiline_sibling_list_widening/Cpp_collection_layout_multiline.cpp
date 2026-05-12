#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::variant<std::map<std::string, std::variant<std::vector<int>, std::vector<std::string>>>, std::vector<std::string>>>{
    {"sibling_lists", std::map<std::string, std::variant<std::vector<int>, std::vector<std::string>>>{
        {"numbers", std::vector<int>{
            1,
            2,
        }},
        {"strings", std::vector<std::string>{
            "x",
            "y",
        }},
    }},
    {"ref_marker_present", std::vector<std::string>{
        "$keep",
        "z",
    }},
};
    (void)my_data;
    return 0;
}
