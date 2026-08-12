#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::variant<std::map<std::string, int>, std::vector<int>>>{
    {"a", std::map<std::string, int>{
        // inner note
        {"b", 1},  // inline b
    }},
    {"list", std::vector<int>{
        1,  // first
        2,  // second
    }},
};
(void)my_data;
my_data = std::map<std::string, std::variant<std::map<std::string, int>, std::vector<int>>>{
    {"a", std::map<std::string, int>{
        // inner note
        {"b", 1},  // inline b
    }},
    {"list", std::vector<int>{
        1,  // first
        2,  // second
    }},
};
    (void)my_data;
    return 0;
}
